/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Build extends Component {

    onClick() {
        this.env.services.action.doAction("erp.action_erp_build");

    }
}

Build.template = xml`
        <button class="btn btn-primary d-flex align-items-center gap-1"
                t-on-click="onClick">
            <i class="fa fa-cogs"/>
            <span>Build</span>
        </button>
`;

registry
    .category("systray")
    .add("build_systray", {
        Component: Build,
        sequence: 10,
    });
