class error(Exception):
    def __str__(self):
        return 'el error es que es igua la 3 el valor proporcionado'
for i in range(5):
    r=i
    try:
        if r==3:
            raise error
        elif r==4:
            raise Exception('SE encotro un error de tipo error')
    except error as e:
         print('eeror encontrado_ ',e)
    except Exception as e:
         print('eeror encontrado_ ',e)
