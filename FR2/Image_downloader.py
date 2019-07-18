#input argument list
# https://google-images-download.readthedocs.io/en/latest/arguments.html

# importing google_images_download module
from google_images_download import google_images_download

# creating object 
response = google_images_download.googleimagesdownload()

# The thing we want to search and download
search_queries = [
    'Ajay Devgn','Akshay Kumar' , 'Aamir Khan' ,'Arnold Schwarzenegger', 'Bruce Willis',
    'Dwayne Johnson' , 'Jackie Chan' , 'Jason Statham' , 'Jet Li' , 'Johnny Depp',
    'Leonardo DiCaprio', 'Salman Khan' , 'Shahrukh Khan' , 'Sylvester Stallone' , 'Tom Cruise',
    'Will Smith'
]


# function for download images from search query

def downloadimages(query):
    # keywords is the search query 
    # format is the image file format 
    # limit is the number of images to be downloaded 
    # print urs is to print the image file url 
    # size is the image size which can be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio of images to download. ("tall, square, wide, panoramic")
    # type Denotes the type of image to be downloaded(face, photo, clip-art, line-drawing, animated)
    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit": 60,
                 "print_urls": True,
                 "size": "medium",
                 "aspect_ratio": "panoramic",
                 "type": "face"}
    try:
        response.download(arguments)

        # Handling File NotFound Error
    except FileNotFoundError:
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit": 4,
                     "print_urls": True,
                     "size": "medium"}

        # Providing arguments for the searched query 
        try:
            # Downloading the photos based 
            # on the given arguments 
            response.download(arguments)
        except:
            pass


# Driver Code
for query in search_queries:
    downloadimages(query)
    print()
