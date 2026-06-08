from odoo import models, fields, api, _
from datetime import date, timedelta

class ContentPlan(models.Model):
    _name = 'content.plan'
    _description = 'Content Plan'
    _order = 'start_date DESC'
    _rec_name = 'name'
    
    name = fields.Char(string='Plan Name', required=True)
    description = fields.Text(string='Description')
    
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)
    
    # Goals and KPIs
    goal = fields.Text(string='Goal')
    target_articles = fields.Integer(string='Target Articles', default=10)
    target_views = fields.Integer(string='Target Views', default=1000)
    
    # Related articles
    article_ids = fields.One2many('content.article', 'plan_id', string='Articles')
    article_count = fields.Integer(string='Articles Count', compute='_compute_article_count')
    
    # Statistics
    published_count = fields.Integer(string='Published', compute='_compute_stats')
    scheduled_count = fields.Integer(string='Scheduled', compute='_compute_stats')
    draft_count = fields.Integer(string='Draft', compute='_compute_stats')
    
    # Team
    team_member_ids = fields.Many2many('res.users', string='Team Members')
    manager_id = fields.Many2one('res.users', string='Plan Manager', default=lambda self: self.env.user)
    
    @api.depends('article_ids')
    def _compute_article_count(self):
        for plan in self:
            plan.article_count = len(plan.article_ids)
    
    @api.depends('article_ids', 'article_ids.status')
    def _compute_stats(self):
        for plan in self:
            plan.published_count = len(plan.article_ids.filtered(lambda a: a.status == 'published'))
            plan.scheduled_count = len(plan.article_ids.filtered(lambda a: a.status == 'scheduled'))
            plan.draft_count = len(plan.article_ids.filtered(lambda a: a.status == 'draft'))
    
    def action_activate(self):
        """Activate the plan"""
        self.status = 'active'
        
    def action_complete(self):
        """Mark plan as completed"""
        self.status = 'completed'
        
    def action_generate_report(self):
        """Generate plan report"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Plan Report: {self.name}',
            'res_model': 'content.plan.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_plan_id': self.id,
            }
        }