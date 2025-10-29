import asyncpg
import asyncio

async def test_connection():
    print("Testing asyncpg connection to Docker PostgreSQL on port 5433...")
    
    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5433,
            user='marketbridge_user',
            password='marketbridge_secure_2025',
            database='marketbridge'
        )
        result = await conn.fetchval("SELECT 'Python connection works!' as test")
        print(f"✅ SUCCESS: {result}")
        await conn.close()
    except Exception as e:
        print(f"❌ FAILED: {e}")

asyncio.run(test_connection())
