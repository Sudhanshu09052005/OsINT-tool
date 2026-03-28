"""
Enhanced PDF Report Generator
Beautiful, professional PDF reports for OSINT investigations
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
                                Table, TableStyle, Image, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import json


class EnhancedPDFReport:
    """Generate beautiful PDF reports"""
    
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section Header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=2,
            borderColor=colors.HexColor('#3f51b5'),
            borderPadding=5,
            backColor=colors.HexColor('#e8eaf6')
        ))
        
        # Subsection
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#3949ab'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Info text
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#212121'),
            spaceAfter=6,
            leading=14
        ))
        
        # Alert/Warning
        self.styles.add(ParagraphStyle(
            name='AlertText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#c62828'),
            spaceAfter=6,
            leading=14,
            backColor=colors.HexColor('#ffebee'),
            borderWidth=1,
            borderColor=colors.HexColor('#ef5350'),
            borderPadding=5
        ))
    
    def add_cover_page(self, data):
        """Add professional cover page"""
        # Title
        title = Paragraph("OSINT INVESTIGATION REPORT", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#424242'),
            alignment=TA_CENTER
        )
        subtitle = Paragraph("Website Reconnaissance & Security Analysis", subtitle_style)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*inch))
        
        # Target information box
        target_domain = data.get('domain', {}).get('domain', 'N/A')
        target_ip = data.get('ip', {}).get('ip', 'N/A')
        
        target_data = [
            ['TARGET INFORMATION', ''],
            ['Domain:', target_domain],
            ['IP Address:', target_ip],
            ['Scan Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        target_table = Table(target_data, colWidths=[3*inch, 3.5*inch])
        target_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#9e9e9e')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(target_table)
        self.story.append(Spacer(1, 1*inch))
        
        # Footer note
        footer_note = Paragraph(
            "<i>This report contains detailed information gathered through OSINT techniques. "
            "For educational and research purposes only.</i>",
            self.styles['InfoText']
        )
        self.story.append(footer_note)
        self.story.append(PageBreak())
    
    def add_executive_summary(self, data):
        """Add executive summary"""
        self.story.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Key findings
        findings = []
        
        # Security Score
        if 'security_headers' in data:
            score = data['security_headers'].get('security_score', 0)
            findings.append(f"Security Score: {score}%")
        
        # Open Ports
        if 'port_scan' in data:
            open_ports = data['port_scan'].get('open_ports', 0)
            findings.append(f"Open Ports Detected: {open_ports}")
        
        # Technologies
        if 'technologies' in data:
            tech_count = len(data['technologies'])
            findings.append(f"Technologies Detected: {tech_count}")
        
        # CMS
        if 'cms' in data:
            cms = data['cms'].get('detected', ['N/A'])[0]
            findings.append(f"CMS Detected: {cms}")
        
        for finding in findings:
            self.story.append(Paragraph(f"• {finding}", self.styles['InfoText']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_domain_info(self, data):
        """Add domain information section"""
        if 'domain' not in data:
            return
        
        self.story.append(Paragraph("DOMAIN INFORMATION", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        domain_info = data['domain']
        
        domain_data = [
            ['Property', 'Value'],
            ['Domain', str(domain_info.get('domain', 'N/A'))],
            ['Registrar', str(domain_info.get('registrar', 'N/A'))],
            ['Creation Date', str(domain_info.get('creation_date', 'N/A'))],
            ['Expiration Date', str(domain_info.get('expiration_date', 'N/A'))],
            ['Updated Date', str(domain_info.get('updated_date', 'N/A'))],
            ['Status', str(domain_info.get('status', 'N/A'))],
        ]
        
        table = self._create_info_table(domain_data)
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_security_analysis(self, data):
        """Add security analysis section"""
        if 'security_headers' not in data:
            return
        
        self.story.append(Paragraph("SECURITY ANALYSIS", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        sec_data = data['security_headers']
        score = sec_data.get('security_score', 0)
        
        # Security score with color
        if score >= 75:
            score_color = colors.HexColor('#4caf50')
            score_text = "GOOD"
        elif score >= 50:
            score_color = colors.HexColor('#ff9800')
            score_text = "MODERATE"
        else:
            score_color = colors.HexColor('#f44336')
            score_text = "POOR"
        
        score_para = Paragraph(
            f"<b>Security Score: {score}% - {score_text}</b>",
            self.styles['SubSection']
        )
        self.story.append(score_para)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Present headers
        if sec_data.get('present'):
            self.story.append(Paragraph("✓ Security Headers Present:", self.styles['SubSection']))
            for header in sec_data['present']:
                text = f"<b>{header['header']}:</b> {header['description']}"
                self.story.append(Paragraph(f"• {text}", self.styles['InfoText']))
        
        # Missing headers
        if sec_data.get('missing'):
            self.story.append(Spacer(1, 0.2*inch))
            self.story.append(Paragraph("✗ Missing Security Headers:", self.styles['SubSection']))
            for header in sec_data['missing']:
                text = f"<b>{header['header']}:</b> {header['description']}"
                self.story.append(Paragraph(f"• {text}", self.styles['AlertText']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_port_scan_results(self, data):
        """Add port scan results"""
        if 'port_scan' not in data or 'error' in data['port_scan']:
            return
        
        self.story.append(Paragraph("PORT SCAN RESULTS", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        port_data = data['port_scan']
        
        summary_text = f"Scanned {port_data.get('scanned_ports', 0)} ports, found {port_data.get('open_ports', 0)} open"
        self.story.append(Paragraph(summary_text, self.styles['InfoText']))
        self.story.append(Spacer(1, 0.1*inch))
        
        if port_data.get('details'):
            port_table_data = [['Port', 'Service', 'Status']]
            for port in port_data['details']:
                port_table_data.append([
                    str(port['port']),
                    port['service'],
                    port['status']
                ])
            
            port_table = Table(port_table_data, colWidths=[1.5*inch, 2*inch, 1.5*inch])
            port_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))
            
            self.story.append(port_table)
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_technologies(self, data):
        """Add detected technologies"""
        if 'technologies' not in data or not data['technologies']:
            return
        
        self.story.append(Paragraph("TECHNOLOGIES DETECTED", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        for tech in data['technologies'][:20]:  # Limit to 20
            self.story.append(Paragraph(f"• {tech}", self.styles['InfoText']))
        
        if len(data['technologies']) > 20:
            self.story.append(Paragraph(
                f"... and {len(data['technologies']) - 20} more",
                self.styles['InfoText']
            ))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_robots_txt(self, data):
        """Add robots.txt analysis"""
        if 'robots_txt' not in data or not data['robots_txt'].get('found'):
            return
        
        self.story.append(Paragraph("ROBOTS.TXT ANALYSIS", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        robots = data['robots_txt']
        
        if robots.get('disallowed_paths'):
            self.story.append(Paragraph("Disallowed Paths:", self.styles['SubSection']))
            for path in robots['disallowed_paths'][:20]:
                self.story.append(Paragraph(f"• {path}", self.styles['InfoText']))
        
        if robots.get('sitemaps'):
            self.story.append(Spacer(1, 0.1*inch))
            self.story.append(Paragraph("Sitemaps:", self.styles['SubSection']))
            for sitemap in robots['sitemaps']:
                self.story.append(Paragraph(f"• {sitemap}", self.styles['InfoText']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_social_media(self, data):
        """Add social media links"""
        if 'social_media' not in data or 'message' in data['social_media']:
            return
        
        self.story.append(Paragraph("SOCIAL MEDIA PRESENCE", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        social = data['social_media']
        for platform, links in social.items():
            self.story.append(Paragraph(f"<b>{platform}:</b>", self.styles['SubSection']))
            for link in links[:5]:  # Limit to 5 per platform
                self.story.append(Paragraph(f"• {link}", self.styles['InfoText']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _create_info_table(self, data):
        """Create a styled information table"""
        table = Table(data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        return table
    
    def generate(self, data):
        """Generate the complete PDF report"""
        self.add_cover_page(data)
        self.add_executive_summary(data)
        self.add_domain_info(data)
        self.add_security_analysis(data)
        self.add_port_scan_results(data)
        self.add_technologies(data)
        self.add_robots_txt(data)
        self.add_social_media(data)
        
        # Build PDF
        self.doc.build(self.story)
        return self.filename
