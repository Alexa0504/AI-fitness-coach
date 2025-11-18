from backend.models import db, Tip
from backend.app import create_app

tips = [
    "Drink 8 glasses of water daily.",
    "Sleep at least 8 hours each night.",
    "Stretch for 5 minutes every morning.",
    "Take a walk during your lunch break.",
    "Stand up and move every hour.",
    "Eat at least 5 servings of fruits and vegetables daily.",
    "Practice deep breathing for 2 minutes.",
    "Limit screen time before bed.",
    "Keep a consistent sleep schedule.",
    "Take short breaks during work to refresh your mind.",
    "Write down 3 things you’re grateful for each day.",
    "Spend 10 minutes meditating daily.",
    "Listen to calming music.",
    "Plan your day the night before.",
    "Avoid multitasking for better focus.",
    "Take the stairs instead of the elevator.",
    "Do a 10-minute bodyweight workout.",
    "Go for a 20-minute walk outdoors.",
    "Try a new physical activity once a week.",
    "Practice good posture while sitting."
]

def seed_tips():
    for t in tips:
        if not db.session.query(Tip).filter_by(text=t).first():
            db.session.add(Tip(category="general", text=t))
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_tips()
        print("✅ Tips seeded successfully!")