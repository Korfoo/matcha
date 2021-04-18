import asyncio
import aioredis
import json

data = {
    'foo': 'bar'
}

async def main():
    conn = await aioredis.create_connection(
        'redis://0.0.0.0', encoding='utf-8')

    ok = await conn.execute('JSON.SET', 'doc', '.', json.dumps(data))
    assert ok == 'OK', ok

    str_value = await conn.execute('JSON.GET', 'doc')
    raw_value = await conn.execute('JSON.GET', 'doc', encoding=None)

    print(json.loads(str_value))
    print(raw_value)
    
    conn.close()
    await conn.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
