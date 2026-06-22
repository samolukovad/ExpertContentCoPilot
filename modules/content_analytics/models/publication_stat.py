from odoo import models, fields

class ContentPublicationStat(models.Model):
    _name = 'content.publication.stat'
    _description = 'Статистика публикации'

    title = fields.Char(string='Название публикации', required=True)
    platform = fields.Selection([
        ('vk', 'VK'),
        ('max', 'Max'),
        ('other', 'Другое'),
    ], string='Площадка', required=True)
    date = fields.Date(string='Дата публикации', required=True)
    views = fields.Integer(string='Просмотры', default=0)
    likes = fields.Integer(string='Лайки', default=0)
    comments = fields.Integer(string='Комментарии', default=0)
    reposts = fields.Integer(string='Репосты', default=0)
    user_id = fields.Many2one('res.users', string='Ответственный', default=lambda self: self.env.user)
