const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const Tb = require('react-icons/tb');
const sharp = require('sharp');

// stage colours from the HL palette, matched to the pipeline node each product sits under
const NAVY_MID = '#1C4470';   // Connect / Master stage
const NAVY_LT  = '#38618B';   // Distribute stage
const TEAL     = '#24B1B1';   // Scout

const icons = [
  ['securities_master', Tb.TbDatabase,      NAVY_MID],
  ['price_master',      Tb.TbTag,           NAVY_MID],
  ['omni',              Tb.TbSnowflake,     NAVY_LT],
  ['ibor',              Tb.TbClockBolt,     NAVY_LT],
  ['scout',             Tb.TbSparkles,      TEAL],
];

(async () => {
  for (const [name, Icon, color] of icons) {
    if (!Icon) { console.error('MISSING icon for', name); process.exit(1); }
    const svg = renderToStaticMarkup(
      React.createElement(Icon, { color, size: 256, strokeWidth: 1.9 })
    );
    await sharp(Buffer.from(svg), { density: 600 })
      .resize(256, 256, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
      .png()
      .toFile(`icons/${name}.png`);
    console.log('wrote icons/' + name + '.png');
  }
})();
