(function () {
  if (location.protocol !== 'file:') return;

  document.getElementById('grid').innerHTML = `<div class="empty-st">
    <b>数据加载失败</b>
    <p>浏览器无法在 file:// 页面读取数据。请通过 HTTP 访问：</p>
    <p>在站点目录运行 <code>python3 -m http.server</code>，然后打开
      <a href="http://localhost:8000/">http://localhost:8000/</a>。</p>
    <p>也可以直接访问 GitHub Pages 网址，页面会正常加载。</p>
  </div>`;
})();
