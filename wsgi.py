import t_tex
handler = t_tex.create_app()


if __name__ == '__main__':
    # Entry point when run via Python interpreter.
    print("== Running in debug mode ==")
    t_tex.create_app().run(host='0.0.0.0', port=8080, debug=True)