import  os
import dotenv

dotenv.load_dotenv()

base_url =os.getenv("BASE_URL")

print(base_url)