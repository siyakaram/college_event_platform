from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, io, smtplib
from email.message import EmailMessage
from reportlab.pdfgen import canvas

Base = declarative_base()
os.makedirs("database", exist_ok=True)
engine = create_engine("sqlite:///database/college.db")
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']
)

# Serve frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
app.mount("/backend/event_backgrounds", StaticFiles(directory="backend/event_backgrounds"), name="event_backgrounds")

# Models
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    lat = Column(Float)
    lon = Column(Float)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    secret_key = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    eligibility = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    radius = Column(Float)
    certificate_template = Column(String)
    background_image = Column(String, nullable=True)

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    attended = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# Student registration
@app.post("/register")
async def register_student(name: str = Form(...), username: str = Form(...),
                           email: str = Form(...), password: str = Form(...),
                           lat: float = Form(...), lon: float = Form(...)):
    db = SessionLocal()
    student = Student(name=name, username=username, email=email, password=password, lat=lat, lon=lon)
    db.add(student)
    db.commit()
    db.close()
    return {"message": "Student registered successfully!"}

# Student login
@app.post("/login")
async def student_login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    student = db.query(Student).filter_by(username=username, password=password).first()
    db.close()
    if student:
        return {"message": "Login successful", "success": True}
    return {"message": "Invalid credentials", "success": False}

# Admin registration
@app.post("/admin/register")
async def admin_register(username: str = Form(...), password: str = Form(...), secret_key: str = Form(...)):
    db = SessionLocal()
    admin = Admin(username=username, password=password, secret_key=secret_key)
    db.add(admin)
    db.commit()
    db.close()
    return {"message": "Admin registered successfully", "success": True}

# Admin login
@app.post("/admin/login")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    admin = db.query(Admin).filter_by(username=username, password=password).first()
    db.close()
    if admin:
        return {"message": "Login successful", "success": True}
    return {"message": "Invalid credentials", "success": False}

# Create event
@app.post("/admin/event/create")
async def create_event(name: str = Form(...), eligibility: str = Form(...),
                       lat: float = Form(...), lon: float = Form(...),
                       radius: float = Form(...),
                       certificate_template: UploadFile = File(...),
                       background_image: UploadFile = File(None)):
    db = SessionLocal()
    os.makedirs("backend/certificates", exist_ok=True)
    template_path = f"backend/certificates/{certificate_template.filename}"
    with open(template_path, "wb") as f:
        f.write(await certificate_template.read())
    bg_path = None
    if background_image:
        os.makedirs("backend/event_backgrounds", exist_ok=True)
        bg_path = f"backend/event_backgrounds/{background_image.filename}"
        with open(bg_path, "wb") as f:
            f.write(await background_image.read())
    event = Event(name=name, eligibility=eligibility, lat=lat, lon=lon,
                  radius=radius, certificate_template=template_path,
                  background_image=bg_path)
    db.add(event)
    db.commit()
    db.close()
    return {"message": f"Event '{name}' created successfully"}

# Get event details
@app.get("/event/{event_id}")
async def get_event(event_id: int):
    db = SessionLocal()
    event = db.query(Event).filter_by(id=event_id).first()
    db.close()
    if not event:
        return {"message": "Event not found"}
    return {
        "id": event.id,
        "name": event.name,
        "eligibility": event.eligibility,
        "lat": event.lat,
        "lon": event.lon,
        "radius": event.radius,
        "background_image": f"/backend/event_backgrounds/{os.path.basename(event.background_image)}" if event.background_image else "background.png"
    }

# Generate certificate
def generate_certificate(student_name, template_path):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.drawString(200, 300, f"Certificate awarded to: {student_name}")
    can.save()
    packet.seek(0)
    return packet.read()

# Send certificate via email
def send_email(to_email, subject, body, pdf_bytes):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "your_email@example.com"
    msg['To'] = to_email
    msg.set_content(body)
    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename="certificate.pdf")
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")
        server.send_message(msg)
