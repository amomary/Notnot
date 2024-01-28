import os
import aminoed              #Rejoint notre serveur discord ou on propose différentes chose comme des vocs, des scripts amino (avec aides), des jeux ect.... -----> https://discord.gg/AhsoukaLegion
import asyncio
from json import loads, dump
from rich.console import Console

console = Console()
def clear(): os.system("cls" if os.name == "nt" else "clear")


async def send_process(web_client: aminoed.WebHttpClient,
                       thread_id: str,
                       thread_title:str,
                       message_type: int,
                       message: str):
    try:
        await asyncio.gather(web_client.send_message(thread_id=thread_id, message=message, type=message_type))
        console.print(f"[bold green]RAID[/]|-- "
                      f"[bold cyan]send message with text[/] {message} [bold cyan]to[/] {thread_title}")
    except:
        pass


@aminoed.run_with_client()
async def main(client: aminoed.Client):
    if "configs.json" not in os.listdir():
        email, password = input("Enter your email >>> "), input("Enter your password >>> ")
        with open("configs.json", "w") as configs_file:
            dump(obj={"email": email, "password": password}, fp=configs_file, indent=4)
    else:
        try:
            configs = loads(open("configs.json").read())
            choice = input(f"Do you want to use saved account:\n"
                           f"email - {configs['email']}\npassword - {configs['password']}\n(Y / N) >>> ").lower()
            if choice == "y":
                email, password = configs["email"], configs["password"]
            else:
                email, password = input("Enter your email >>> "), input("Enter your password >>> ")
                with open("configs.json", "w") as configs_file:
                    dump(obj={"email": email, "password": password}, fp=configs_file, indent=4)
        except KeyError:
            os.remove("configs.json")
            email, password = input("Enter your email >>> "), input("Enter your password >>> ")
            with open("configs.json", "w") as configs_file:
                dump(obj={"email": email, "password": password}, fp=configs_file, indent=4)
    await client.login(email=email,
                       password=password)
    clear()
    console.print(f"[bold magenta]Successfully[/] logged in with [bold cyan]{client.auth.account.email}[/]")
    console.print(f"\n[bold yellow]Enter the community link[/]\n[bold cyan]>>>[/] ", end="")
    link = input()
    console.print(f"\n[bold yellow]Enter the message to spam[/]\n[bold cyan]>>>[/] ", end="")
    message = input()
    console.print(f"\n[bold yellow]Enter the message type[/]\n[bold cyan]>>>[/] ", end="")
    message_type = int(input())
    ndc_id = (await client.get_link_info(link)).community.ndcId
    await client.join_community(ndc_id=ndc_id)
    await client.set_community(community=ndc_id)
    chats = await client.get_public_chat_threads()
    web_client = aminoed.WebHttpClient(ndc_id=ndc_id, sid=client.auth.sid)
    await asyncio.gather(*[web_client.join_chat(thread_id=thread.threadId) for thread in chats])
    while True:
        try:
            await asyncio.gather(
                *[send_process(web_client=web_client,
                               thread_id=thread.threadId,
                               thread_title=thread.title,
                               message_type=message_type,
                               message=message) for thread in chats])
        except KeyboardInterrupt:
            break
    console.print(f"[bold magenta]Thanks for using, bye!!![/]")
    exit()
