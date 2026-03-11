/** @odoo-module **/

import { Component, xml, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { router } from "@web/core/browser/router";
import { user } from "@web/core/user";

export class Build extends Component {
  setup() {
    this.isDebug = Boolean(odoo.debug);
    this.state = useState({ isErpAdmin: false });

    onWillStart(async () => {
      this.state.isErpAdmin = await user.hasGroup("erp.group_erp_admin");
    });
  }
  async onClickBuild() {
    await this.env.services.action.doAction("erp.action_erp_build");
  }

  async onClickBug() {
    let debug = this.isDebug ? 0 : "assets";
    router.pushState({ debug: debug }, { reload: true });
  }
}

Build.template = xml`
<div class="d-flex flex-row" t-if="state.isErpAdmin">
    <button class="btn text-white d-flex align-items-center gap-1"
        t-on-click="onClickBuild"
        t-if="isDebug"
    >
        <i class="fa fa-cogs"/>
        <span>Build</span>
    </button>

    <button class="btn text-white d-flex align-items-center justify-content-center"
        t-on-click="onClickBug"
        title="Bug"
    >
        <i class="fa fa-lock" t-if="!isDebug"/>
        <i class="fa fa-unlock-alt" t-if="isDebug"/>
    </button>
</div>
`;

registry.category("systray").add("build_systray", {
  Component: Build,
  sequence: 10,
});
