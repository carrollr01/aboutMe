const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const Tb = require('react-icons/tb');
const sharp = require('sharp');

// stage colours from the HL palette, matched to the pipeline node each product sits under
// all icons share the label colour: theme accent6, pale blue on navy
const PALE = '#9FC3DA';

const icons = [
  ['securities_master', Tb.TbDatabase,  PALE],
  ['price_master',      Tb.TbTag,       PALE],
  ['omni',              Tb.TbSnowflake, PALE],
  ['ibor',              Tb.TbClockBolt, PALE],
  ['scout',             Tb.TbSparkles,  PALE],
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
