import discord
from discord.ext import commands
from textblob import TextBlob
import csv
import re


intents = discord.Intents.default()
# mendeteksi saat ada user yang sedang mengetik
intents.typing = True
# mendeteksi saat ada user yang sedang online
intents.presences = False

# awalan yang harus digunakan jika ingin memicu perintah bot
bot = commands.Bot(command_prefix='.', intents=intents)

# hanya untuk mencetak nama bot ini saat bot sudah diaktifkan (hanya bisa dilihat di terminal saja)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# sebelum data kata dideteksi oleh library textblob, data tersebut akan masuk ke sini untuk dihilangkan alfanumerik, huruf besar, dan baru ke masuk kedalam textblob.
def preprocess_text(text):
    text = re.sub(r"[^\w\s@]", "", text)  # Menghapus karakter non-alphanumerik kecuali "@"
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b\d+\b", "", text)  # Menghapus urutan angka
    text = text.lower()
    return text

@bot.command()
async def check(ctx, *, text):
    # data yang diterima akan diproses menggunakan fungsi preprocess_text yang telah dijelaskan sebelumnya.
    preprocessed_text = preprocess_text(text)
    # data yang telah melalui proses preprocessing akan diberikan sebagai input untuk objek TextBlob, setelah dikoreksi data akan akan diubah menjadi str(string) menggunakan fungsi str()
    corrected_text = str(TextBlob(preprocessed_text).correct())
    
    # Menghapus tanda "@" dari input sebelum menulis ke file CSV
    cleaned_text = text.replace("@", "")
    
    # dengan menggunakan ctx(context) bot akan mengirim pesan ke user yang memanggil perintah tersebut sebuah pesan dengan isi kata yang sudah dikoreksi
    await ctx.channel.send(f'Corrected text: {corrected_text}')
    # fungsi ini akan menginput data yang kita ketik dan juga menulis kata yang telah dikoreksi ke dalam csv
    with open("output.csv", mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([cleaned_text, corrected_text])

# fungsi ini ada agar tidak terjadi looping, jadi bot hanya mengdeteksi pesan dari user bukan pesan dari bot itu sendiri
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

bot.run('MTExNjM0NDg3Mjc1MjkwNjI4MA.GU8rG4.Hf02JacCrnJY_UDmrttheZbxkxqUqCSOro3aTw')