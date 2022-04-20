import numpy as np

class Graph:
    playlist = []
    artists = {}
    density = []
    popularity = []
    correlation = []
    total_track = 0

    def __init__(self, playlist=None, popularity=None):
        if playlist == None:
            pass
        else:
            self.popularity = popularity
            self.total_track = len(playlist)
            self.playlist = playlist
            for i, artist in enumerate(playlist):
                found = False
                for a in artist:
                    if a in self.artists:
                        self.artists[a].append(i)
                        found = True
                    break
                if not found:
                    #self.artists[artist[0]] = []
                    self.artists[artist.values()] = i

    # density = artist_appeared/total_tracks
    def get_density(self):
        for a in self.playlist:
            # b = a[0]
            b = list(a.values())[1]
            if self.artists.get(b[0]):
                self.density.append(len(self.artists[b[0]])/self.total_track)
            else:
                self.density.append(1/self.total_track)
        return self.density

    # calculate from seed track
    def get_correlation(self, track):
        pivot_artist = self.playlist[track]
        # count tracks with significant density
        self.get_density()
        density_condition = np.quantile(self.density, 0.75)
        count = sum(1 for i in self.density if i > density_condition)
        if count == 0:
            step = 0
        else:
            step = 1/count
        step_count = 1
        for i, a in enumerate(self.playlist):
            if pivot_artist == a:
                corr = 1
            else:
                # calculate correlation for track with significant popularity difference
                diff = self.popularity[track] - self.popularity[i]
                diff = abs(diff)
                if self.popularity[track] == 0:
                    corr = 0
                else:
                    corr = (diff/self.popularity[track])

                if self.density[i] > 0.02:
                    corr = corr + step * step_count
                    step_count = step_count + 1
            self.correlation.append([corr, i])
        return self.correlation
