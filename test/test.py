import os
import time
import requests
from assertpy import assert_that

QHOME = os.environ["QHOME"]

def start_backend_q():
  os.system(QHOME + "/l32/q backend.q &")


def kill_backend_q():
  os.system("pkill -f \"" + QHOME + "/l32/q backend.q\"")


def default_path():
  res = requests.get("http://localhost:8000/")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Hello there, my favourite browser:  python-requests/2.19.1")


def hello():
  res = requests.get("http://localhost:8000/hello")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("hello")


def json():
  res = requests.get("http://localhost:8000/json")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to({"a":1,"b":2,"c":3})


def goodbye():
  res = requests.post("http://localhost:8000/goodbye", json={"name":"python"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Goodbye now python")


def cookie():
  session = requests.Session()
  res = session.get("http://localhost:8000/cookie")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Check your cookies!")
  assert_that(session.cookies.get_dict()).is_equal_to({"sid":"s355IonT0k3n"})


def cors():
  # The preflight request must pass
  headers = { "access-control-request-method": "GET" , "access-control-request-headers": "Content-Type" }
  options = requests.options("http://localhost:8000/cors", headers=headers)
  assert_that(options.headers["Access-Control-Allow-Origin"]).is_equal_to("http://localhost:3000")
  assert_that(options.headers["Access-Control-Allow-Methods"]).is_equal_to("GET")
  assert_that(options.headers["Access-Control-Allow-Headers"]).is_equal_to("Content-Type")
  assert_that(options.status_code).is_equal_to(200)

  # And also the browser must be assured that the response was intended for them
  get = requests.get("http://localhost:8000/cors")
  assert_that(get.headers["Access-Control-Allow-Origin"]).is_equal_to("http://localhost:3000")
  assert_that(get.status_code).is_equal_to(200)


def run_test(test_name, test):
  try:
    print("- " + test_name)
    test()
  except AssertionError as e:
    print("fail\n\t" + str(e))


def tests():
  run_test("default_path", default_path)
  run_test("hello", hello)
  run_test("json", json)
  run_test("goodbye", goodbye)
  run_test("cookie", cookie)
  run_test("cors", cors)


def main():
    print("=== starting backend ===")
    start_backend_q()
    time.sleep(1)

    print("=== starting tests ===")
    tests()

    print("=== killing backend ===")
    kill_backend_q()

    print("=== finished tests ===")


main()
exit(0)
