from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0003_placecards_alter_itineraries_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='placecards',
            unique_together=set(),
        ),
    ]