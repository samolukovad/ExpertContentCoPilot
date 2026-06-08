from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime

class ContentArticle(models.Model):
    _name = 'content.article'
    _description = 'Content Article'
    _order = 'publish_date DESC, create_date DESC'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Basic fields
    title = fields.Char(string='Title', required=True, tracking=True)
    text = fields.Html(string='Content', required=True, tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('revision', 'Revision Needed'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', required=True, tracking=True)
    date = fields.Date(string='Creation Date', default=fields.Date.today, required=True)
    
    # Workflow specific fields
    idea_id = fields.Many2one('content.idea', string='Source Idea', ondelete='set null')
    publish_date = fields.Date(string='Publish Date', tracking=True)
    scheduled_date = fields.Date(string='Scheduled Date', tracking=True)
    
    # Content metadata
    category = fields.Selection([
        ('blog', 'Blog Post'),
        ('article', 'Article'),
        ('social', 'Social Media Post'),
        ('presentation', 'Presentation'),
        ('training', 'Training Material'),
        ('other', 'Other')
    ], string='Category', default='article')
    
    tags = fields.Char(string='Tags')
    keywords = fields.Char(string='SEO Keywords')
    word_count = fields.Integer(string='Word Count', compute='_compute_word_count', store=True)
    
    # AI recommendations (to be implemented with AI service)
    ai_suggestions = fields.Text(string='AI Suggestions')
    structure_score = fields.Float(string='Structure Score', digits=(3, 2))
    
    # Analytics
    views = fields.Integer(string='Views', default=0)
    likes = fields.Integer(string='Likes', default=0)
    shares = fields.Integer(string='Shares', default=0)
    comments = fields.Integer(string='Comments', default=0)
    
    # Version control
    version = fields.Integer(string='Version', default=1)
    parent_article_id = fields.Many2one('content.article', string='Parent Version')
    version_ids = fields.One2many('content.article', 'parent_article_id', string='Versions')
    
    # Plan relationships
    plan_id = fields.Many2one('content.plan', string='Content Plan')
    
    # User fields
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user)
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    @api.depends('text')
    def _compute_word_count(self):
        for record in self:
            if record.text:
                # Rough word count for HTML content
                import re
                text = re.sub(r'<[^>]+>', ' ', record.text)
                record.word_count = len(text.split())
            else:
                record.word_count = 0
    
    @api.constrains('publish_date')
    def _check_publish_date(self):
        for record in record:
            if record.publish_date and record.publish_date < fields.Date.today():
                raise ValidationError("Publish date cannot be in the past")
    
    def action_submit_review(self):
        """Submit article for review"""
        self.status = 'in_review'
        
    def action_approve(self):
        """Approve article"""
        self.status = 'scheduled'
        
    def action_publish(self):
        """Publish article"""
        self.status = 'published'
        self.publish_date = fields.Date.today()
        
    def action_schedule(self):
        """Schedule article"""
        self.status = 'scheduled'
        
    def action_create_new_version(self):
        """Create a new version of this article"""
        self.ensure_one()
        new_article = self.copy({
            'title': f"{self.title} (v{self.version + 1})",
            'status': 'draft',
            'version': self.version + 1,
            'parent_article_id': self.id,
            'publish_date': False,
            'scheduled_date': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'content.article',
            'res_id': new_article.id,
            'view_mode': 'form',
        }