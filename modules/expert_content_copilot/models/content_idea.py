from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class ContentIdea(models.Model):
    _name = 'content.idea'
    _description = 'Content Idea'
    _order = 'create_date DESC'
    _rec_name = 'title'
    
    # Basic fields
    title = fields.Char(string='Title', required=True, tracking=True)
    text = fields.Text(string='Description', required=True, tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', required=True, tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    
    # Additional fields for better UX
    tags = fields.Char(string='Tags', help='Comma-separated tags')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], string='Priority', default='medium')
    
    source = fields.Char(string='Source', help='Where this idea came from')
    expected_impact = fields.Text(string='Expected Impact')
    
    # Relationships
    article_ids = fields.One2many('content.article', 'idea_id', string='Articles')
    article_count = fields.Integer(string='Articles Count', compute='_compute_article_count')
    
    # Company and user fields
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    @api.depends('article_ids')
    def _compute_article_count(self):
        for record in self:
            record.article_count = len(record.article_ids)
    
    @api.constrains('title')
    def _check_title_length(self):
        for record in self:
            if len(record.title) < 3:
                raise ValidationError("Title must be at least 3 characters long")
    
    def action_create_article(self):
        """Create an article from this idea"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Article',
            'res_model': 'content.article',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_idea_id': self.id,
                'default_title': self.title,
                'default_text': self.text,
                'default_status': 'draft'
            }
        }