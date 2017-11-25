import core
import requests
from core import bitcoin_balance

service = core.Service("bitcoin-service")
app = core.app
core.set_service(service)


@app.route("/update_cover")
def update_cover():
	for group in service.mongo.find({"activation":True}):
		new_btc_value = float(bitcoin_balance(group["fields"]["bitcoin_adress"]))
		old_btc_value = service.get_varible(group["group_id"], "btc")
		
		if new_btc_value == old_btc_value:
			return "ok", 200
		
		service.set_varible(group["group_id"], "btc", new_btc_value)
		service.update_image(group["group_id"])
	return "ok", 200

if __name__ == "__main__":
	app.run()
