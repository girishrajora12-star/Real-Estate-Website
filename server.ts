import express, { Request, Response } from 'express';
import path from 'path';
import fs from 'fs';
import { execFile } from 'child_process';
import { fileURLToPath } from 'url';
import https from 'https';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
  const isProd = process.env.NODE_ENV === 'production';

  app.use(express.json({ limit: '50mb' }));

  const assetsDir = path.resolve(__dirname, 'public', 'assets');
  const framesDir = path.join(assetsDir, 'frames');
  const defaultVideoName = 'Home Walkthrough Video.mp4';
  const defaultVideoPath = path.join(assetsDir, defaultVideoName);

  // Dedicated upload helper page to easily drag-and-drop the video
  app.get('/upload', (_req: Request, res: Response) => {
    res.setHeader('Content-Type', 'text/html');
    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Upload Home Walkthrough Video</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0E0D0B; color: #F3EFE6; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }
    .card { background: #1A1916; border: 1px solid rgba(255,255,255,0.14); border-radius: 20px; padding: 36px; max-width: 580px; width: 100%; box-shadow: 0 30px 60px rgba(0,0,0,0.7); }
    .badge { color: #F2A24B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; }
    h1 { font-size: 26px; font-weight: 500; margin: 6px 0 14px 0; color: #FFF; }
    p { font-size: 14px; line-height: 1.6; color: #A6A095; margin-bottom: 24px; }
    .dropzone { border: 2px dashed rgba(242, 162, 75, 0.45); background: rgba(242, 162, 75, 0.04); border-radius: 16px; padding: 40px 20px; text-align: center; cursor: pointer; transition: all 0.2s; }
    .dropzone:hover, .dropzone.active { border-color: #F2A24B; background: rgba(242, 162, 75, 0.1); }
    .drop-title { font-size: 16px; font-weight: 600; color: #FFF; margin-bottom: 6px; }
    .drop-sub { font-size: 13px; color: #A6A095; }
    .progress-box { margin-top: 20px; display: none; }
    .progress-bar { height: 8px; background: rgba(255,255,255,0.1); border-radius: 99px; overflow: hidden; }
    .progress-fill { height: 100%; width: 0%; background: #F2A24B; transition: width 0.15s; }
    .status-text { margin-top: 10px; font-size: 13px; color: #F2A24B; }
    .btn-return { display: none; margin-top: 24px; width: 100%; padding: 14px; background: #F2A24B; color: #0E0D0B; text-align: center; font-weight: 600; border-radius: 12px; text-decoration: none; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">VIDEO WALKTHROUGH PIPELINE</div>
    <h1>Upload Home Walkthrough Video</h1>
    <p>Select or drop <strong>Home Walkthrough Video.mp4</strong> here. Our Python ffmpeg engine will wipe old frames, extract every frame, and immediately refresh the landing page!</p>
    
    <div class="dropzone" id="dz">
      <input type="file" id="fileInput" accept="video/mp4,video/*" style="display:none;" />
      <div style="font-size: 40px; margin-bottom: 8px;">🎬</div>
      <div class="drop-title">Drop "Home Walkthrough Video.mp4" here</div>
      <div class="drop-sub">or click to browse from your computer</div>
    </div>

    <div class="progress-box" id="pbox">
      <div class="progress-bar"><div class="progress-fill" id="pfill"></div></div>
      <div class="status-text" id="stext">Uploading video...</div>
    </div>

    <a href="/" class="btn-return" id="btnReturn">✨ View Updated Landing Page</a>
  </div>

  <script>
    const dz = document.getElementById('dz');
    const fi = document.getElementById('fileInput');
    const pbox = document.getElementById('pbox');
    const pfill = document.getElementById('pfill');
    const stext = document.getElementById('stext');
    const btnReturn = document.getElementById('btnReturn');

    dz.addEventListener('click', () => fi.click());
    dz.addEventListener('dragover', (e) => { e.preventDefault(); dz.classList.add('active'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('active'));
    dz.addEventListener('drop', (e) => {
      e.preventDefault();
      dz.classList.remove('active');
      if (e.dataTransfer.files.length) upload(e.dataTransfer.files[0]);
    });
    fi.addEventListener('change', () => {
      if (fi.files.length) upload(fi.files[0]);
    });

    function upload(file) {
      pbox.style.display = 'block';
      pfill.style.width = '0%';
      stext.textContent = 'Uploading ' + file.name + '...';

      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/api/upload-video', true);
      xhr.setRequestHeader('x-filename', file.name || 'Home Walkthrough Video.mp4');

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          const pct = Math.round((e.loaded / e.total) * 90);
          pfill.style.width = pct + '%';
          if (pct >= 90) stext.textContent = 'Extracting frames with ffmpeg (clearing old frames)...';
        }
      };

      xhr.onload = () => {
        if (xhr.status === 200) {
          pfill.style.width = '100%';
          stext.textContent = '✅ Frames successfully extracted! The landing page is ready.';
          btnReturn.style.display = 'block';
        } else {
          stext.textContent = 'Error: ' + xhr.responseText;
        }
      };
      xhr.onerror = () => { stext.textContent = 'Upload network error.'; };
      xhr.send(file);
    }
  </script>
</body>
</html>`);
  });

  // Status check endpoint
  app.get('/api/frames-status', (_req: Request, res: Response) => {
    try {
      const manifestPath = path.join(framesDir, 'manifest.json');
      let manifest = null;
      if (fs.existsSync(manifestPath)) {
        manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      }
      const videoExists = fs.existsSync(defaultVideoPath);
      const videoSize = videoExists ? fs.statSync(defaultVideoPath).size : 0;
      const frameFiles = fs.existsSync(framesDir)
        ? fs.readdirSync(framesDir).filter(f => f.startsWith('frame_') && f.endsWith('.jpg'))
        : [];

      return res.json({
        ok: true,
        videoExists,
        videoSize,
        frameCount: frameFiles.length,
        manifest,
      });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err.message });
    }
  });

  // Extract frames helper
  const runExtraction = (videoPath: string): Promise<string> => {
    return new Promise((resolve, reject) => {
      const scriptPath = path.resolve(__dirname, 'scripts', 'extract_video_frames.py');
      execFile('python3', [scriptPath, videoPath], (error, stdout, stderr) => {
        if (error) {
          return reject(new Error(stderr || stdout || error.message));
        }
        resolve(stdout);
      });
    });
  };

  // Direct Binary Video Upload Endpoint (handles large video files smoothly)
  app.post('/api/upload-video', (req: Request, res: Response) => {
    try {
      const filename = (req.headers['x-filename'] as string) || defaultVideoName;
      const cleanFilename = path.basename(filename);
      const targetPath = path.join(assetsDir, cleanFilename);

      if (!fs.existsSync(assetsDir)) {
        fs.mkdirSync(assetsDir, { recursive: true });
      }

      const writeStream = fs.createWriteStream(targetPath);
      req.pipe(writeStream);

      writeStream.on('finish', async () => {
        try {
          const stats = fs.statSync(targetPath);
          if (stats.size === 0) {
            return res.status(400).json({ ok: false, error: 'Uploaded file is 0 bytes.' });
          }

          const stdout = await runExtraction(targetPath);
          return res.json({
            ok: true,
            message: `Extracted frames from ${cleanFilename}`,
            size: stats.size,
            log: stdout,
          });
        } catch (extractErr: any) {
          return res.status(500).json({
            ok: false,
            error: `Video uploaded but frame extraction failed: ${extractErr.message}`,
          });
        }
      });

      writeStream.on('error', (err) => {
        return res.status(500).json({ ok: false, error: err.message });
      });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err.message });
    }
  });

  // Download video from URL (e.g. Hugging Face Space / Direct link)
  app.post('/api/extract-url', async (req: Request, res: Response) => {
    const { url } = req.body;
    if (!url || typeof url !== 'string') {
      return res.status(400).json({ ok: false, error: 'url is required' });
    }

    try {
      const targetPath = defaultVideoPath;
      const fileStream = fs.createWriteStream(targetPath);
      const client = url.startsWith('https') ? https : http;

      client.get(url, (response) => {
        if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
          // Handle redirect
          const redirectUrl = response.headers.location;
          const redirectClient = redirectUrl.startsWith('https') ? https : http;
          redirectClient.get(redirectUrl, (redResp) => {
            redResp.pipe(fileStream);
            fileStream.on('finish', async () => {
              try {
                const log = await runExtraction(targetPath);
                return res.json({ ok: true, message: 'Downloaded & extracted frames successfully', log });
              } catch (e: any) {
                return res.status(500).json({ ok: false, error: e.message });
              }
            });
          });
          return;
        }

        response.pipe(fileStream);
        fileStream.on('finish', async () => {
          try {
            const log = await runExtraction(targetPath);
            return res.json({ ok: true, message: 'Downloaded & extracted frames successfully', log });
          } catch (e: any) {
            return res.status(500).json({ ok: false, error: e.message });
          }
        });
      }).on('error', (err) => {
        return res.status(500).json({ ok: false, error: err.message });
      });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err.message });
    }
  });

  // Trigger manual extraction on already uploaded video
  app.post('/api/trigger-extract', async (_req: Request, res: Response) => {
    try {
      let target = defaultVideoPath;
      if (!fs.existsSync(target)) {
        const mp4s = fs.readdirSync(assetsDir).filter(f => f.endsWith('.mp4'));
        if (mp4s.length > 0) {
          target = path.join(assetsDir, mp4s[0]);
        } else {
          return res.status(404).json({ ok: false, error: 'No .mp4 video found in public/assets.' });
        }
      }
      const log = await runExtraction(target);
      return res.json({ ok: true, log });
    } catch (err: any) {
      return res.status(500).json({ ok: false, error: err.message });
    }
  });

  // Mount Vite or static
  if (!isProd) {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'custom',
    });
    app.use(vite.middlewares);
    app.use('*', async (req, res, next) => {
      const url = req.originalUrl;
      try {
        let template = fs.readFileSync(path.resolve(__dirname, 'index.html'), 'utf-8');
        template = await vite.transformIndexHtml(url, template);
        res.status(200).set({ 'Content-Type': 'text/html' }).end(template);
      } catch (e: any) {
        vite.ssrFixStacktrace(e);
        next(e);
      }
    });
  } else {
    app.use(express.static(path.resolve(__dirname, 'dist')));
    app.get('*', (_req, res) => {
      res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running at http://0.0.0.0:${PORT}`);
  });
}

startServer();
