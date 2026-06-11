# 🚀 Expert Content CoPilot

<div align="center">

**Цифровой ассистент для системного создания экспертного контента**

[![Odoo](https://img.shields.io/badge/Odoo-19.0-714B67?logo=odoo)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-LGPL--3-7D4698)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/samolukovad/ExpertContentCoPilot)

*Превращает хаос идей в стройную систему контент-планирования*

</div>

---

## 📋 О проекте

**Expert Content CoPilot** — это Odoo-модуль, который помогает экспертам и компаниям системно создавать, хранить и развивать профессиональный контент: статьи, выступления, посты и обучающие материалы.

Ассистент превращает процесс создания материалов в понятную систему — как project-менеджер, но для экспертного контента.

### 🎯 Цель проекта

Сделать управление экспертным контентом простым и структурированным. Платформа помогает планировать публикации, отслеживать темы и превращать идеи в полноценные материалы.

### ✨ Что меняет модуль

- Экспертный контент перестаёт теряться в заметках и файлах
- Появляется единая система планирования публикаций
- Повышается качество и регулярность выхода материалов

---


---

## 🗃️ Модели данных

### 1. Content Idea (Идея контента)

| Поле | Тип | Описание |
|------|-----|----------|
| `title` | Char | Название идеи |
| `text` | Text | Описание |
| `status` | Selection | Статус (draft/approved/completed) |
| `date` | Date | Дата создания |
| `user_id` | Many2one | Ответственный |
| `article_ids` | One2many | Связанные статьи |

**Workflow:** Идея → Доработка → Создание статьи

### 2. Content Article (Статья)

| Поле | Тип | Описание |
|------|-----|----------|
| `title` | Char | Заголовок статьи |
| `text` | Html | Содержимое |
| `status` | Selection | Статус (draft/published) |
| `date` | Date | Дата публикации |
| `author_id` | Many2one | Автор |
| `idea_id` | Many2one | Источник идея |
| `plan_id` | Many2one | Привязка к плану |

**Workflow:** Черновик → На ревью → Опубликовано

### 3. Content Plan (План контента)

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | Char | Название плана |
| `description` | Text | Описание |
| `date` | Date | Дата плана |
| `manager_id` | Many2one | Менеджер |
| `article_ids` | One2many | Статьи в плане |

**Workflow:** План → Активен → Завершён

---

## 🚀 Установка

### Предварительные требования

- Odoo 19.0
- Python 3.11+
- PostgreSQL 15+

### 1. Скопируйте модуль

```bash
# Скопируйте папку модуля в директорию addons Odoo
cp -r expert_content_copilot /path/to/odoo/addons/

cd /path/to/odoo
python odoo-bin --addons-path=addons --db_user=odoo --db_password=123456


Установка модуля: 
Откройте http://localhost:8069

Перейдите в Apps

Удалите фильтр "Apps"

Найдите "Expert Content CoPilot"

Нажмите Install