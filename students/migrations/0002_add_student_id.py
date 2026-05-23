from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
