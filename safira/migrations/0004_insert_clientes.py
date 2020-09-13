from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safira', '0003_cliente_limite_credito'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO safira_cliente (account_id, nome, email, renda, telefone, data_nascimento, sexo, perfil_investidor)
            VALUES ("00711234511", "Susan Wojcicki da Silva", "susan.wokcicki@example.com", 5000, "+5511911111111", "1983-09-16", "F", "conservador"),
            ("00711234522", "Satya Nadella da Silva", "satya.nadella@example.com", 12500, "+5519222222222", "1972-08-06", "F", "moderado");
            """
        )
    ]
