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
from datetime import datetime, timedelta
import os


class PDFGenerator:
    """Générateur de rapports PDF pour l'imprimerie"""
    
    def __init__(self, model):
        self.model = model
        
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
        stats = self.model.calculer_solde(date)
        est_cloture = self.model.verifier_cloture(date)
        
        resume_titre = Paragraph("<b>RÉSUMÉ FINANCIER</b>", 
                                ParagraphStyle('ResumeTitre', parent=styles['Heading2'], 
                                             fontName='Times-Bold', fontSize=14, 
                                             textColor=colors.black, 
                                             leading=21, spaceAfter=12))
        elements.append(resume_titre)
        
        # Calculer les différents types de transactions
        transactions_temp = self.model.obtenir_transactions(date)
        depenses_normales_montant = sum([t[2] for t in transactions_temp if t[1] == 'depense' and (len(t) < 7 or t[6] == 'normale')])
        depenses_caisse_montant = sum([t[2] for t in transactions_temp if t[1] == 'depense' and len(t) >= 7 and t[6] == 'speciale'])
        apports_montant = sum([t[2] for t in transactions_temp if t[1] == 'apport'])
        
        solde_jour = stats['recettes'] - depenses_normales_montant
        solde_avec_caisse = solde_jour + apports_montant - depenses_caisse_montant
        
        resume_data = [
            ['DÉSIGNATION', 'MONTANT (FC)'],
            ['Recette du jour', f"{stats['recettes']:,.0f}"],
            ['Dépenses (Normales)', f"{depenses_normales_montant:,.0f}"],
            ['Dépenses de la caisse', f"{depenses_caisse_montant:,.0f}"],
            ['Apports en capital', f"{apports_montant:,.0f}"],
            ['Solde du jour', f"{solde_jour:,.0f}"],
            ['Solde avec caisse', f"{solde_avec_caisse:,.0f}"]
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
            ('FONTNAME', (0, -2), (-1, -2), 'Times-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold')
        ]))
        
        elements.append(resume_table)
        elements.append(Spacer(1, 1*cm))
        
        # Détail des transactions
        transactions = self.model.obtenir_transactions(date)
        
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
    
    def generer_rapport_mensuel(self, date_debut, date_fin, nom_fichier, mois_nom, annee):
        """Générer un rapport PDF mensuel avec détail par semaine"""
        
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
            leading=24,
            alignment=1
        )
        
        # Style pour le texte normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=18,
            alignment=0
        )
        
        # En-tête
        elements.append(Paragraph("BUREAUTIQUE", title_style))
        elements.append(Paragraph(f"Rapport Mensuel - {mois_nom} {annee}", title_style))
        
        # Date de génération
        date_generation = datetime.now().strftime("%d/%m/%Y à %H:%M")
        elements.append(Paragraph(f"Généré le {date_generation}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Période
        date_debut_formatted = datetime.strptime(date_debut, "%Y-%m-%d").strftime("%d/%m/%Y")
        date_fin_formatted = datetime.strptime(date_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
        elements.append(Paragraph(f"<b>Période:</b> du {date_debut_formatted} au {date_fin_formatted}", normal_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # Obtenir les statistiques pour la période
        stats = self.model.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.model.verifier_cloture(date)]
        
        if stats_clotures:
            # Calculer les totaux
            total_recettes = sum(rec for _, rec, _, _, _ in stats_clotures)
            total_depenses = sum(dep_norm for _, _, dep_norm, _, _ in stats_clotures)
            total_dep_caisse = sum(dep_caisse for _, _, _, dep_caisse, _ in stats_clotures)
            total_apports = sum(apport for _, _, _, _, apport in stats_clotures)
            total_resultat = total_recettes - total_depenses
            solde_avec_caisse = total_recettes - total_depenses + total_apports - total_dep_caisse
            
            # Tableau récapitulatif
            recap_data = [
                ['', 'Montant'],
                ['Recettes totales', f"{total_recettes:,.0f} FC"],
                ['Dépenses totales', f"{total_depenses:,.0f} FC"],
                ['Dépenses de la caisse', f"{total_dep_caisse:,.0f} FC"],
                ['Apports en capital', f"{total_apports:,.0f} FC"],
                ['Résultat (Recettes - Dépenses)', f"{total_resultat:,.0f} FC"],
                ['Solde avec caisse', f"{solde_avec_caisse:,.0f} FC"]
            ]
            
            recap_table = Table(recap_data, colWidths=[10*cm, 7*cm])
            recap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(recap_table)
            elements.append(Spacer(1, 1*cm))
            
            # Grouper par semaine
            from collections import defaultdict
            semaines = defaultdict(lambda: {'recettes': 0, 'depenses': 0, 'dep_caisse': 0, 'apports': 0, 'debut_semaine': None, 'fin_semaine': None})
            
            for date_str, recettes, depenses, dep_caisse, apports in stats_clotures:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                # Calculer le lundi de la semaine (début de semaine)
                lundi = date_obj - timedelta(days=date_obj.weekday())
                # Calculer le dimanche de la semaine (fin de semaine)
                dimanche = lundi + timedelta(days=6)
                
                # Utiliser le lundi comme clé pour identifier la semaine
                cle_semaine = lundi.strftime("%Y-%m-%d")
                
                semaines[cle_semaine]['recettes'] += recettes
                semaines[cle_semaine]['depenses'] += depenses
                semaines[cle_semaine]['dep_caisse'] += dep_caisse
                semaines[cle_semaine]['apports'] += apports
                
                # Stocker le début et fin de semaine
                if semaines[cle_semaine]['debut_semaine'] is None:
                    semaines[cle_semaine]['debut_semaine'] = lundi
                    semaines[cle_semaine]['fin_semaine'] = dimanche
            
            # Tableau détaillé par semaine
            elements.append(Paragraph("<b>Détail par semaine:</b>", normal_style))
            elements.append(Spacer(1, 0.5*cm))
            
            detail_data = [['Semaine', 'Période', 'Recettes', 'Dépenses', 'Dép. Caisse', 'Apports', 'Solde']]
            
            # Trier les semaines par ordre chronologique
            for cle_semaine in sorted(semaines.keys()):
                data = semaines[cle_semaine]
                
                debut = data['debut_semaine']
                fin = data['fin_semaine']
                
                # Formater la période (Lundi - Dimanche)
                periode = f"{debut.strftime('%d/%m')} - {fin.strftime('%d/%m')}"
                
                # Calculer le numéro de semaine ISO
                semaine_num = debut.isocalendar()[1]
                
                # Solde = Recettes - Dépenses + Apports - Dép. Caisse
                solde = data['recettes'] - data['depenses'] + data['apports'] - data['dep_caisse']
                
                detail_data.append([
                    f"S{semaine_num}",
                    periode,
                    f"{data['recettes']:,.0f} FC",
                    f"{data['depenses']:,.0f} FC",
                    f"{data['dep_caisse']:,.0f} FC",
                    f"{data['apports']:,.0f} FC",
                    f"{solde:,.0f} FC"
                ])
            
            detail_table = Table(detail_data, colWidths=[1.8*cm, 2.8*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 11)
            ]))
            
            elements.append(detail_table)
            
        else:
            elements.append(Paragraph("Aucun rapport clôturé pour cette période.", normal_style))
        
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
    
    def generer_rapport_periode(self, date_debut, date_fin, nom_fichier, type_periode):
        """Générer un rapport PDF pour une période (hebdomadaire, mensuel, annuel)"""
        
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
            leading=24,
            alignment=1
        )
        
        # Style pour le texte normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=18,
            alignment=0
        )
        
        # En-tête
        elements.append(Paragraph("BUREAUTIQUE", title_style))
        elements.append(Paragraph(f"Rapport {type_periode}", title_style))
        
        # Date de génération
        date_generation = datetime.now().strftime("%d/%m/%Y à %H:%M")
        elements.append(Paragraph(f"Généré le {date_generation}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Période
        date_debut_formatted = datetime.strptime(date_debut, "%Y-%m-%d").strftime("%d/%m/%Y")
        date_fin_formatted = datetime.strptime(date_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
        elements.append(Paragraph(f"<b>Période:</b> du {date_debut_formatted} au {date_fin_formatted}", normal_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # Obtenir les statistiques pour la période
        stats = self.model.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.model.verifier_cloture(date)]
        
        if stats_clotures:
            # Calculer les totaux
            total_recettes = sum(rec for _, rec, _, _, _ in stats_clotures)
            total_depenses = sum(dep_norm for _, _, dep_norm, _, _ in stats_clotures)
            total_dep_caisse = sum(dep_caisse for _, _, _, dep_caisse, _ in stats_clotures)
            total_apports = sum(apport for _, _, _, _, apport in stats_clotures)
            total_resultat = total_recettes - total_depenses
            solde_avec_caisse = total_recettes - total_depenses + total_apports - total_dep_caisse
            
            # Tableau récapitulatif
            recap_data = [
                ['', 'Montant'],
                ['Recettes totales', f"{total_recettes:,.0f} FC"],
                ['Dépenses totales', f"{total_depenses:,.0f} FC"],
                ['Dépenses de la caisse', f"{total_dep_caisse:,.0f} FC"],
                ['Apports en capital', f"{total_apports:,.0f} FC"],
                ['Résultat (Recettes - Dépenses)', f"{total_resultat:,.0f} FC"],
                ['Solde avec caisse', f"{solde_avec_caisse:,.0f} FC"]
            ]
            
            recap_table = Table(recap_data, colWidths=[10*cm, 7*cm])
            recap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(recap_table)
            elements.append(Spacer(1, 1*cm))
            
            # Tableau détaillé par jour
            elements.append(Paragraph("<b>Détail par jour:</b>", normal_style))
            elements.append(Spacer(1, 0.5*cm))
            
            detail_data = [['Date', 'Recettes', 'Dépenses', 'Dép. Caisse', 'Apports', 'Solde']]
            
            for date, recettes, depenses, dep_caisse, apports in stats_clotures:
                date_formatted = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
                solde = recettes - depenses + apports - dep_caisse
                detail_data.append([
                    date_formatted,
                    f"{recettes:,.0f} FC",
                    f"{depenses:,.0f} FC",
                    f"{dep_caisse:,.0f} FC",
                    f"{apports:,.0f} FC",
                    f"{solde:,.0f} FC"
                ])
            
            detail_table = Table(detail_data, colWidths=[2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 11)
            ]))
            
            elements.append(detail_table)
            
        else:
            elements.append(Paragraph("Aucun rapport clôturé pour cette période.", normal_style))
        
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
    
    def generer_rapport_annuel(self, date_debut, date_fin, nom_fichier, annee):
        """Générer un rapport PDF annuel avec synthèse mensuelle"""
        
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
            leading=24,
            alignment=1
        )
        
        # Style pour le texte normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=18,
            alignment=0
        )
        
        # En-tête
        elements.append(Paragraph("BUREAUTIQUE", title_style))
        elements.append(Paragraph(f"Rapport Annuel - {annee}", title_style))
        
        # Date de génération
        date_generation = datetime.now().strftime("%d/%m/%Y à %H:%M")
        elements.append(Paragraph(f"Généré le {date_generation}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Période
        elements.append(Paragraph(f"<b>Année:</b> {annee}", normal_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # Obtenir les statistiques pour l'année
        stats = self.model.obtenir_statistiques_detaillees_par_jour(date_debut, date_fin)
        
        # Filtrer uniquement les jours clôturés
        stats_clotures = [(date, rec, dep_norm, dep_caisse, apport) 
                          for date, rec, dep_norm, dep_caisse, apport in stats 
                          if self.model.verifier_cloture(date)]
        
        if stats_clotures:
            # Calculer les totaux annuels
            total_recettes = sum(rec for _, rec, _, _, _ in stats_clotures)
            total_depenses = sum(dep_norm for _, _, dep_norm, _, _ in stats_clotures)
            total_dep_caisse = sum(dep_caisse for _, _, _, dep_caisse, _ in stats_clotures)
            total_apports = sum(apport for _, _, _, _, apport in stats_clotures)
            # Résultat = Recettes - Dépenses normales (les dépenses caisse et apports n'affectent pas le résultat journalier)
            # Mais on affiche le solde final en tenant compte de la caisse
            total_resultat = total_recettes - total_depenses
            solde_avec_caisse = total_recettes - total_depenses + total_apports - total_dep_caisse
            
            # Tableau récapitulatif annuel
            recap_data = [
                ['', 'Montant'],
                ['Recettes totales', f"{total_recettes:,.0f} FC"],
                ['Dépenses totales', f"{total_depenses:,.0f} FC"],
                ['Dépenses de la caisse', f"{total_dep_caisse:,.0f} FC"],
                ['Apports en capital', f"{total_apports:,.0f} FC"],
                ['Résultat (Recettes - Dépenses)', f"{total_resultat:,.0f} FC"],
                ['Solde avec caisse', f"{solde_avec_caisse:,.0f} FC"]
            ]
            
            recap_table = Table(recap_data, colWidths=[10*cm, 7*cm])
            recap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(recap_table)
            elements.append(Spacer(1, 1*cm))
            
            # Grouper par mois
            from collections import defaultdict
            mois = defaultdict(lambda: {'recettes': 0, 'depenses': 0, 'dep_caisse': 0, 'apports': 0})
            
            for date_str, recettes, depenses, dep_caisse, apports in stats_clotures:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                # Utiliser l'année-mois comme clé
                cle_mois = date_obj.strftime("%Y-%m")
                
                mois[cle_mois]['recettes'] += recettes
                mois[cle_mois]['depenses'] += depenses
                mois[cle_mois]['dep_caisse'] += dep_caisse
                mois[cle_mois]['apports'] += apports
            
            # Tableau synthèse mensuelle
            elements.append(Paragraph("<b>Synthèse mensuelle:</b>", normal_style))
            elements.append(Spacer(1, 0.5*cm))
            
            detail_data = [['Mois', 'Recettes', 'Dépenses', 'Dép. Caisse', 'Apports', 'Solde']]
            
            # Noms des mois en français
            noms_mois = {
                '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
                '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
                '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
            }
            
            # Trier les mois par ordre chronologique
            for cle_mois in sorted(mois.keys()):
                data = mois[cle_mois]
                
                # Extraire le numéro du mois
                annee_num, mois_num = cle_mois.split('-')
                nom_mois = noms_mois.get(mois_num, mois_num)
                
                # Solde = Recettes - Dépenses + Apports - Dépenses Caisse
                solde = data['recettes'] - data['depenses'] + data['apports'] - data['dep_caisse']
                
                detail_data.append([
                    nom_mois,
                    f"{data['recettes']:,.0f} FC",
                    f"{data['depenses']:,.0f} FC",
                    f"{data['dep_caisse']:,.0f} FC",
                    f"{data['apports']:,.0f} FC",
                    f"{solde:,.0f} FC"
                ])
            
            detail_table = Table(detail_data, colWidths=[2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.83, 0.83, 0.83)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 11)
            ]))
            
            elements.append(detail_table)
            
        else:
            elements.append(Paragraph("Aucun rapport clôturé pour cette année.", normal_style))
        
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
