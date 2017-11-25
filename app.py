import core
import requests

service = core.Service("bitcoin-service")
app = core.app
core.set_service(service)


def bitcoin_balance(address):
	if not address: return 0 

	try:
		res = requests.get("https://blockchain.info/balance?active=%s" % address).json()

		balance = res[address]["final_balance"]
		res = requests.get("https://blockchain.info/ticker").json()

		currency = res["RUB"]["buy"]
		return round(balance*currency/10**8,2)
	except Exception:
		return 0


@app.route("/update_cover")
def update_cover():
	for group in service.mongo.find({"activation":True}):
		new_btc_value = int(bitcoin_balance(group["fields"]["bitcoin_adress"]))
		old_btc_value = service.get_varible(group["group_id"], "btc")
		
		if new_btc_value == old_btc_value:
			return "ok", 200
		
		service.set_varible(group["group_id"], "btc", new_btc_value)
		service.update_image(group["group_id"])
	return "ok", 200

if __name__ == "__main__":
	app.run()
