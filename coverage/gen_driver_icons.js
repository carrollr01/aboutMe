const path = require('path');
const fs = require('fs');
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const Tb = require('react-icons/tb');
const sharp = require('sharp');

// slide 3's accent blue, used for the demand-driver icons
const BLUE = process.argv[2] || '#0067A5';

const icons = [
  ['dd_ai',        Tb.TbSparkles],
  ['dd_reg',       Tb.TbScale],
  ['dd_volume',    Tb.TbDatabase],
  ['dd_cloud',     Tb.TbCloudUp],
  ['dd_blindspot', Tb.TbZoomQuestion],
];

(async () => {
  for (const [name, Icon] of icons) {
    if (!Icon) { console.error('MISSING', name); process.exit(1); }
    const svg = renderToStaticMarkup(
      React.createElement(Icon, { color: BLUE, size: 256, strokeWidth: 1.9 }));
    fs.writeFileSync(path.join(__dirname, 'icons', `${name}.svg`), svg);
    await sharp(Buffer.from(svg), { density: 600 })
      .resize(256, 256, { fit: 'contain',
                          background: { r: 255, g: 255, b: 255, alpha: 0 } })
      .png().toFile(path.join(__dirname, 'icons', `${name}.png`));
    console.log('wrote', name, BLUE);
  }
})();
