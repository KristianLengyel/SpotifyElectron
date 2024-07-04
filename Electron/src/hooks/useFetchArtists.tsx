import { useState, useEffect } from 'react';
import Global from 'global/global';
import defaultThumbnailPlaylist from '../assets/imgs/DefaultThumbnailPlaylist.jpg';

interface PropsArtistCard {
  name: string;
  photo: string;
}

const useFetchArtists = () => {
  const [artists, setArtists] = useState<PropsArtistCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${Global.backendBaseUrl}artists/`);
        if (!response.ok) {
          throw new Error(`Failed to fetch Artists`);
        }

        const data = await response.json();
        if (data.artists) {
          const propsArtists: PropsArtistCard[] = data.artists.map(
            (artist: any) => ({
              name: artist.name,
              photo:
                artist.photo === '' ? defaultThumbnailPlaylist : artist.photo,
            }),
          );
          setArtists(propsArtists);
        }
      } catch (err) {
        console.log('Failed to fetch artists:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { artists, loading };
};

export default useFetchArtists;
