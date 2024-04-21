import wave

def split_wav(path):
    with wave.open(path, 'rb') as f:
        params = f.getparams()
        bytes_per_frame = params.sampwidth * params.nchannels

        chunks = []
        with open(path, 'rb') as file:
            while True:
                chunk = file.read(256 * bytes_per_frame)
                if not chunk:
                    break

                chunks.append(chunk)
        return chunks
