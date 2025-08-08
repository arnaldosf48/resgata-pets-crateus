import db_setup 
from login_window import abrir_login
from dashboard_window import abrir_dashboard

if __name__ == "__main__": 
    abrir_login(on_success=abrir_dashboard)
 