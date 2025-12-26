{
    "name": "ERP",
    "version": "1.0",
    "author": "Hieu",
    "summary": "ERP",
    "depends": ["mail"],
    "data": [
        "security/role.xml",
        "security/ir.model.access.csv",
        "views/build.xml",
    ],
    "application": True,
    "assets": {
        "web.assets_backend": [
            "erp/static/src/**",
        ],
    },
}
