import { AnalysisWorkerWrapper, createWorker, Paper } from 'yoastseo';
import WithContext from './WithContext';
import ResultContainers from './ResultContainers';

export default class Panel extends WithContext {
  constructor(context) {
    super(context);
    this.workerUrl = `${this.baseUrl}/static/wagtailyoast/dist/js/yoastworker${this.context.version}.js`;
    this.worker = new AnalysisWorkerWrapper(createWorker(this.workerUrl));
  }

  static async getPreviewPageContent() {
    const $form = $('#page-edit-form');
    const $previewBtn = $('button[class^="button action-preview"');
    const previewUrl = $previewBtn.data('action');
    await $.ajax({
      url: previewUrl,
      method: 'POST',
      data: new FormData($form[0]),
      processData: false,
      contentType: false,
    });
    const result = await $.ajax({
      url: previewUrl,
      type: 'GET',
    });
    return result;
  }

  async syncPanel() {
    const paper = new Paper(await Panel.getPreviewPageContent(), {
      keyword: this.$yoastKeywords.val(),
      title: this.$yoastTitle.val(),
      description: this.$yoastSearchDescription.val(),
      slug: this.$yoastSlug.val(),
      titleWidth: 500, // FIXME: How to get width of title in pixel? https://github.com/Yoast/javascript/blob/master/packages/yoastseo/src/values/Paper.js#L29
    });
    const containers = new ResultContainers(await this.worker.analyze(paper));
    containers.sync();
  }

  init() {
    this.worker.initialize({
      locale: this.context.locale,
      contentAnalysisActive: true,
      keywordAnalysisActive: true,
      logLevel: 'ERROR',
    }).then(() => {
      this.$yoastPanel = $('#yoast_panel');
      this.$yoastKeywords = this.$yoastPanel.find('#yoast_keywords');
      this.$yoastTitle = $(`#id_${this.$yoastPanel.find('#yoast_title').data('field')}`);
      this.$yoastSearchDescription = $(`#id_${this.$yoastPanel.find('#yoast_search_description').data('field')}`);
      this.$yoastSlug = $(`#id_${this.$yoastPanel.find('#yoast_slug').data('field')}`);

      const keyUpElements = [
        this.$yoastKeywords,
      ];

      // Key up of inputs (keywords)

      Array.prototype.forEach.call(keyUpElements, ($el) => {
        $el.on('keyup', async (e) => {
          e.preventDefault();
          await this.syncPanel();
        });
      });

      // Click on yoast pannel

      $('li[aria-controls="tab-yoast"]').click(async (e) => {
        e.preventDefault();
        await this.syncPanel();
      });

      this.syncPanel();
    });
  }
}
