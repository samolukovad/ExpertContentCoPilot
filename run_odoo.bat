@echo off
call F:\miniconda3\Scripts\activate.bat
call conda activate odoo17
cd /d F:\ExpertContentCoPilot\odoo
python odoo-bin -u expert_content_copilot --db_user=odoo --db_password=123456 --db_host=localhost
pause