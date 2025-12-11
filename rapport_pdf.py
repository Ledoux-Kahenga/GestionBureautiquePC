"""
Génération de rapports PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os


class GenerateurRapportPDF:
    """Classe pour générer des rapports PDF"""
    
    def __init__(self, database):
        self.db = database
        
    def generer_rapport_journalier(self, date, nom_fichier):
        """Générer un rapport PDF pour une journée"""
        
        # Créer le document PDF
        doc = SimpleDocTemplate(
            nom_fichier,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Conteneur pour les éléments du PDF
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Style pour le titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Times-Bold',
            fontSize=16,
            textColor=colors.black,
            spaceAfter=30,
            leading=24,  # interligne 1.5 (16 * 1.5)
            alignment=1  # Centre
        )
        
        # Style pour les sous-titres
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontName='Times-Bold',
            fontSize=12,
            textColor=colors.black,
            spaceAfter=12,
            leading=18,  # interligne 1.5 (12 * 1.5)
            alignment=1
        )
        
        # Style pour le texte normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=18,  # interligne 1.5 (12 * 1.5)
            spaceAfter=6
        )
        
        # En-tête du rapport
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_formatee = date_obj.strftime("%A %d %B %Y")
        
        titre = Paragraph(f"<b>RAPPORT JOURNALIER</b>", title_style)
        elements.append(titre)
        
        sous_titre = Paragraph(f"{date_formatee}", subtitle_style)
        elements.append(sous_titre)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Résumé financier
        stats = self.db.calculer_solde(date)
        est_cloture = self.db.verifier_cloture(date)
        
        resume_titre = Paragraph("<b>RÉSUMÉ FINANCIER</b>", 
                                ParagraphStyle('ResumeTitre', parent=styles['Heading2'], 
                                             fontName='Times-Bold', fontSize=14, 
                                             textColor=colors.black, 
                                             leading=21, spaceAfter=12))
        elements.append(resume_titre)
        
        # Calculer uniquement les dépenses normales
        transactions_temp = self.db.obtenir_transactions(date)
        depenses_normales_montant = sum([t[2] for t in transactions_temp if t[1] == 'depense' and (len(t) < 7 or t[6] == 'normale')])
        
        resume_data = [
            ['DÉSIGNATION', 'MONTANT (FC)'],
            ['Recette du jour', f"{stats['recettes']:,.0f}"],
            ['Dépenses (Normales)', f"{depenses_normales_montant:,.0f}"],
            ['Solde', f"{stats['recettes'] - depenses_normales_montant:,.0f}"]
        ]
        
        resume_table = Table(resume_data, colWidths=[12*cm, 5*cm])
        resume_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 3), (-1, 3), 'Times-Bold')
        ]))
        
        elements.append(resume_table)
        elements.append(Spacer(1, 1*cm))
        
        # Détail des transactions
        transactions = self.db.obtenir_transactions(date)
        
        if transactions:
            detail_titre = Paragraph("<b>DÉTAIL DEPENSES</b>", 
                                    ParagraphStyle('DetailTitre', parent=styles['Heading2'], 
                                                 fontName='Times-Bold', fontSize=14, 
                                                 textColor=colors.black, 
                                                 leading=21, spaceAfter=12))
            elements.append(detail_titre)
            
            # Filtrer uniquement les dépenses normales
            depenses_normales = [t for t in transactions if t[1] == 'depense' and (len(t) < 7 or t[6] == 'normale')]
            
            # Section Détails des dépenses (normales)
            if depenses_normales:
                depenses_titre = Paragraph("<b>Dépenses</b>", 
                                          ParagraphStyle('DepensesTitre', parent=styles['Heading3'], 
                                                       fontName='Times-Bold', fontSize=12, 
                                                       textColor=colors.black, 
                                                       leading=18, spaceAfter=8))
                elements.append(depenses_titre)
                
                depenses_data = [['N°', 'HEURE', 'DESCRIPTION', 'MONTANT (FC)']]
                total_depenses_normales = 0
                
                for idx, transaction in enumerate(depenses_normales, 1):
                    id_trans, type_trans, montant, description, date_t, created_at = transaction[:6]
                    heure = created_at.split()[1] if len(created_at.split()) > 1 else ""
                    depenses_data.append([
                        str(idx),
                        heure[:5],  # HH:MM
                        description or '-',
                        f"{montant:,.0f}"
                    ])
                    total_depenses_normales += montant
                
                # Ajouter le sous-total
                depenses_data.append(['', '', 'Total', f"{total_depenses_normales:,.0f}"])
                
                depenses_table = Table(depenses_data, colWidths=[1.5*cm, 2.5*cm, 10*cm, 3*cm])
                depenses_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    # Style pour le sous-total
                    ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold'),
                    ('FONTSIZE', (0, -1), (-1, -1), 12),
                    ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.black)
                ]))
                
                elements.append(depenses_table)
                elements.append(Spacer(1, 0.8*cm))
        
        else:
            elements.append(Paragraph("Aucune transaction pour cette journée.", normal_style))
        
        # Pied de page
        elements.append(Spacer(1, 2*cm))
        
        signature_data = [
            ['', ''],
            ['Signature du responsable', 'Cachet de l\'établissement']
        ]
        
        signature_table = Table(signature_data, colWidths=[8.5*cm, 8.5*cm])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('LINEABOVE', (0, 0), (0, 0), 0.5, colors.black),
            ('LINEABOVE', (1, 0), (1, 0), 0.5, colors.black),
        ]))
        
        elements.append(signature_table)
        
        # Générer le PDF
        doc.build(elements)
        
        return nom_fichier
