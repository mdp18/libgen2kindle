import configparser, json, requests, sys, subprocess
def main():
    #path = './Atomic habits.mobi'
    #extension = path.split('.')[-1]
    #cmd = './ebook-convert ' + path + ' ' + path + '.epub'
    cmd = './ebook-convert "./Atomic habits.mobi" "./Atomic habits.epub"'
    process = subprocess.Popen(['Calibre2\ebook-convert','./Atomic habits.mobi','./Atomic habits.epub'],stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
    process.wait()
    print("Done")

main()