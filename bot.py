import asyncio
from main import main
from src.utils.logger import logger


if __name__ == "__main__":
    logger.info("Starting bot...")
    
    asyncio.run(main())
