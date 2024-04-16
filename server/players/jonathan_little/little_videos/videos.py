


def little_videos():
  return [
    "https://www.youtube.com/watch?v=1S8F3Afs2dg",
    "https://www.youtube.com/watch?v=LXOlTggaQkE",
    "https://www.youtube.com/watch?v=JLgQEmaer-s",
    "&index=1",
    "https://www.youtube.com/watch?v=X2SUTZEOoIk&list=PLMYHGfD_v6wuED06SS8H2-7wkc3hR41pp&index=3",
    
  ]

def little_coaching():
  base_url = "https://www.youtube.com/watch?v=Xu9NwBz2GEc&list=PLMYHGfD_v6wuED06SS8H2-7wkc3hR41pp"
  return [f"{base_url}&index={i}" for i in range(1, 63)]


