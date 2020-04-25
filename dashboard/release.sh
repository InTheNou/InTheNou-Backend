curl -s https://api.github.com/repos/InTheNou/InTheNou-AdminDashboard/releases/latest \
| grep "browser_download_url.*zip" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -


unzip dist.zip 

rm dist.zip