"""Replace legacy square placeholders with themed emoji icons."""
from django.db import migrations


ICONS = {
    "club": "🤝",
    "event": "🎯",
    "galleryitem": "📸",
    "update": "📣",
    "helptopic": "🆘",
}


def set_emoji_icons(apps, schema_editor):
    for model_name, emoji in ICONS.items():
        model = apps.get_model("core", model_name)
        model.objects.filter(icon="■").update(icon=emoji)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_club_icon_alter_event_icon_and_more"),
    ]

    operations = [
        migrations.RunPython(set_emoji_icons, migrations.RunPython.noop),
    ]
