from flask import Flask, request,render_template
app=Flask("__name__")

@app.route("/")
def return_file():
	return  render_template("ajax1.html");
@app.route("/order_food/")
def order_food():
	return render_template("ajax_echo.html");
@app.route("/foodstore/")
def echo():
	print(request.args.get("food"))
	return request.args.get("food")



if __name__=="__main__":
	app.run(debug=True)
