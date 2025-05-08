```python
from flask import Flask, render_template, request, send_file, url_for
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def devis():
    if request.method == 'POST':
        # Récupération des données du formulaire
        client  = request.form['client']
        travaux = request.form['travaux']
        surface = float(request.form['surface'] or 0)
        tarif   = float(request.form['tarif'] or 0)
        tva     = float(request.form['tva'] or 0)
        duree   = request.form['duree']
        marge   = float(request.form['marge'] or 0)

        # Calculs
        total_ht  = surface * tarif + marge
        total_tva = total_ht * (tva / 100)
        total_ttc = total_ht + total_tva

        # Génère le HTML du devis
        html = render_template('devis.html',
            client=client,
            travaux=travaux,
            surface=surface,
            tarif=tarif,
            tva=tva,
            duree=duree,
            marge=marge,
            total_ht=total_ht,
            total_tva=total_tva,
            total_ttc=total_ttc,
            logo_url=url_for('static', filename='logo.png')
        )

        # Génération du PDF en mémoire
        pdf = io.BytesIO()
        HTML(string=html, base_url=request.base_url).write_pdf(pdf)
        pdf.seek(0)

        # Renvoi du PDF en pièce jointe
        return send_file(
            pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'devis_{client.replace(" ", "_")}.pdf'
        )

    # GET → formulaire
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---
