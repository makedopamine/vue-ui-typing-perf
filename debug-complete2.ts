import { setup } from './utils';
import * as path from 'path';
import * as fs from 'fs';

(async () => {
  const context = await setup(path.join(__dirname, 'servers'), {
    'v2.1.6': { npm: '@vue/language-server@2.1.6', bin: './bin/vue-language-server.js' },
  });
  const folder = path.join(__dirname, 'temp', 'element-plus@2.3.4');
  fs.writeFileSync(path.join(folder, 'App.vue'), [
    `<script lang="ts">`,
    `import {} from 'element-plus';`,
    `w`,
    `</script>`,
  ].join('\n'));

  await context.start({ rootPath: folder, repeatTimes: 1 }, async (connection, _timekeeper, helpers) => {
    connection.onRequest('client/registerCapability', () => {});
    connection.onRequest('workspace/configuration', () => {});

    await helpers.initialize({ typescript: { tsdk: path.join(__dirname, 'node_modules', 'typescript', 'lib') } });
    const document = await helpers.openDocument('./App.vue', 'vue');
    const pos = document.positionAt(document.getText().indexOf('\nw\n') + 2);
    const completeResult: any = await helpers.requestCompletion(document, pos);
    const items = completeResult?.items ?? [];
    console.log('items length:', items.length);
    console.log('has watch:', items.some((i: any) => i?.label === 'watch'));
    console.log('first labels:', items.slice(0, 40).map((i: any) => i?.label).join(', '));
  });
})();
