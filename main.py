from sys import argv


def main():
    # I know the philisophers over at Python will be very angry but 
    # In order to unnessesarily import what is not needed..
    if argv[1] == 'create':
        from create import create
        create()
        return

    if argv[1] == 'run':
        from run import run
        run()
        return

    if argv[1] == 'check':
        from check import check
        check()
        return

    if argv[1] == 'help':
        from saidia import saidia
        saidia()
        return

              
if __name__ == "__main__":
    main()
