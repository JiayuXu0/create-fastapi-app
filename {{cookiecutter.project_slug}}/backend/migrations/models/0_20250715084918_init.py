from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "api" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "path" VARCHAR(100) NOT NULL /* API路径 */,
    "method" VARCHAR(6) NOT NULL /* 请求方法 */,
    "summary" VARCHAR(500) NOT NULL /* 请求简介 */,
    "tags" VARCHAR(100) NOT NULL /* API标签 */
);
CREATE INDEX IF NOT EXISTS "idx_api_created_78d19f" ON "api" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_api_updated_643c8b" ON "api" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_api_path_9ed611" ON "api" ("path");
CREATE INDEX IF NOT EXISTS "idx_api_method_a46dfb" ON "api" ("method");
CREATE INDEX IF NOT EXISTS "idx_api_summary_400f73" ON "api" ("summary");
CREATE INDEX IF NOT EXISTS "idx_api_tags_04ae27" ON "api" ("tags");
CREATE TABLE IF NOT EXISTS "audit_log" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL /* 用户ID */,
    "username" VARCHAR(64) NOT NULL DEFAULT '' /* 用户名称 */,
    "module" VARCHAR(64) NOT NULL DEFAULT '' /* 功能模块 */,
    "summary" VARCHAR(128) NOT NULL DEFAULT '' /* 请求描述 */,
    "method" VARCHAR(10) NOT NULL DEFAULT '' /* 请求方法 */,
    "path" VARCHAR(255) NOT NULL DEFAULT '' /* 请求路径 */,
    "status" INT NOT NULL DEFAULT -1 /* 状态码 */,
    "response_time" INT NOT NULL DEFAULT 0 /* 响应时间(单位ms) */,
    "request_args" JSON /* 请求参数 */,
    "response_body" JSON /* 返回数据 */
);
CREATE INDEX IF NOT EXISTS "idx_audit_log_created_277f5d" ON "audit_log" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_audit_log_updated_4bb07a" ON "audit_log" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_audit_log_user_id_d5b3c4" ON "audit_log" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_audit_log_usernam_b6341e" ON "audit_log" ("username");
CREATE INDEX IF NOT EXISTS "idx_audit_log_module_a9ee07" ON "audit_log" ("module");
CREATE INDEX IF NOT EXISTS "idx_audit_log_summary_88bf13" ON "audit_log" ("summary");
CREATE INDEX IF NOT EXISTS "idx_audit_log_method_2525a0" ON "audit_log" ("method");
CREATE INDEX IF NOT EXISTS "idx_audit_log_path_39c3ce" ON "audit_log" ("path");
CREATE INDEX IF NOT EXISTS "idx_audit_log_status_60fba5" ON "audit_log" ("status");
CREATE INDEX IF NOT EXISTS "idx_audit_log_respons_1e56a2" ON "audit_log" ("response_time");
CREATE TABLE IF NOT EXISTS "dept" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL UNIQUE /* 部门名称 */,
    "desc" VARCHAR(500) /* 备注 */,
    "is_deleted" INT NOT NULL DEFAULT 0 /* 软删除标记 */,
    "order" INT NOT NULL DEFAULT 0 /* 排序 */,
    "parent_id" INT NOT NULL DEFAULT 0 /* 父部门ID */
);
CREATE INDEX IF NOT EXISTS "idx_dept_created_4b11cf" ON "dept" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_dept_updated_0c0bd1" ON "dept" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_dept_name_c2b9da" ON "dept" ("name");
CREATE INDEX IF NOT EXISTS "idx_dept_is_dele_466228" ON "dept" ("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_dept_order_ddabe1" ON "dept" ("order");
CREATE INDEX IF NOT EXISTS "idx_dept_parent__a71a57" ON "dept" ("parent_id");
CREATE TABLE IF NOT EXISTS "deptclosure" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ancestor" INT NOT NULL /* 父代 */,
    "descendant" INT NOT NULL /* 子代 */,
    "level" INT NOT NULL DEFAULT 0 /* 深度 */
);
CREATE INDEX IF NOT EXISTS "idx_deptclosure_created_96f6ef" ON "deptclosure" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_updated_41fc08" ON "deptclosure" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_ancesto_fbc4ce" ON "deptclosure" ("ancestor");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_descend_2ae8b1" ON "deptclosure" ("descendant");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_level_ae16b2" ON "deptclosure" ("level");
CREATE TABLE IF NOT EXISTS "file_mapping" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file_id" VARCHAR(255) NOT NULL UNIQUE /* 文件ID */,
    "original_filename" VARCHAR(255) NOT NULL /* 原始文件名 */,
    "file_type" VARCHAR(50) NOT NULL /* 文件类型 */,
    "file_size" BIGINT /* 文件大小(字节) */,
    "upload_user_id" INT NOT NULL /* 上传用户ID */,
    "file_path" VARCHAR(500) /* 本地文件路径 */
) /* 文件映射模型 - 管理文件ID和文件信息的映射关系 */;
CREATE INDEX IF NOT EXISTS "idx_file_mappin_created_519929" ON "file_mapping" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_updated_621dab" ON "file_mapping" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_file_id_35e02a" ON "file_mapping" ("file_id");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_upload__3562e4" ON "file_mapping" ("upload_user_id");
CREATE TABLE IF NOT EXISTS "menu" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL /* 菜单名称 */,
    "remark" JSON /* 保留字段 */,
    "menu_type" VARCHAR(7) /* 菜单类型 */,
    "icon" VARCHAR(100) /* 菜单图标 */,
    "path" VARCHAR(100) NOT NULL /* 菜单路径 */,
    "order" INT NOT NULL DEFAULT 0 /* 排序 */,
    "parent_id" INT NOT NULL DEFAULT 0 /* 父菜单ID */,
    "is_hidden" INT NOT NULL DEFAULT 0 /* 是否隐藏 */,
    "component" VARCHAR(100) NOT NULL /* 组件 */,
    "keepalive" INT NOT NULL DEFAULT 1 /* 存活 */,
    "redirect" VARCHAR(100) /* 重定向 */
);
CREATE INDEX IF NOT EXISTS "idx_menu_created_b6922b" ON "menu" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_menu_updated_e6b0a1" ON "menu" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_menu_name_b9b853" ON "menu" ("name");
CREATE INDEX IF NOT EXISTS "idx_menu_path_bf95b2" ON "menu" ("path");
CREATE INDEX IF NOT EXISTS "idx_menu_order_606068" ON "menu" ("order");
CREATE INDEX IF NOT EXISTS "idx_menu_parent__bebd15" ON "menu" ("parent_id");
CREATE TABLE IF NOT EXISTS "role" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL UNIQUE /* 角色名称 */,
    "desc" VARCHAR(500) /* 角色描述 */
);
CREATE INDEX IF NOT EXISTS "idx_role_created_7f5f71" ON "role" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_role_updated_5dd337" ON "role" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_role_name_e5618b" ON "role" ("name");
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(20) NOT NULL UNIQUE /* 用户名称 */,
    "alias" VARCHAR(30) /* 姓名 */,
    "email" VARCHAR(255) NOT NULL UNIQUE /* 邮箱 */,
    "phone" VARCHAR(20) /* 电话 */,
    "password" VARCHAR(128) /* 密码 */,
    "is_active" INT NOT NULL DEFAULT 1 /* 是否激活 */,
    "is_superuser" INT NOT NULL DEFAULT 0 /* 是否为超级管理员 */,
    "last_login" TIMESTAMP /* 最后登录时间 */,
    "dept_id" INT /* 部门ID */
);
CREATE INDEX IF NOT EXISTS "idx_user_created_b19d59" ON "user" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_user_updated_dfdb43" ON "user" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
CREATE INDEX IF NOT EXISTS "idx_user_alias_6f9868" ON "user" ("alias");
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE INDEX IF NOT EXISTS "idx_user_phone_4e3ecc" ON "user" ("phone");
CREATE INDEX IF NOT EXISTS "idx_user_is_acti_83722a" ON "user" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_user_is_supe_b8a218" ON "user" ("is_superuser");
CREATE INDEX IF NOT EXISTS "idx_user_last_lo_af118a" ON "user" ("last_login");
CREATE INDEX IF NOT EXISTS "idx_user_dept_id_d4490b" ON "user" ("dept_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "role_menu" (
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "menu_id" BIGINT NOT NULL REFERENCES "menu" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_role_menu_role_id_90801c" ON "role_menu" ("role_id", "menu_id");
CREATE TABLE IF NOT EXISTS "role_api" (
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "api_id" BIGINT NOT NULL REFERENCES "api" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_role_api_role_id_ba4286" ON "role_api" ("role_id", "api_id");
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_user_role_user_id_d0bad3" ON "user_role" ("user_id", "role_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
