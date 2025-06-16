import logging

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_log(user_id, article):
    logging.info(f"User {user_id} requested article: {article}")