from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "api" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "path" VARCHAR(100) NOT NULL,
    "method" VARCHAR(6) NOT NULL,
    "summary" VARCHAR(500) NOT NULL,
    "tags" VARCHAR(100) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_api_created_78d19f" ON "api" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_api_updated_643c8b" ON "api" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_api_path_9ed611" ON "api" ("path");
CREATE INDEX IF NOT EXISTS "idx_api_method_a46dfb" ON "api" ("method");
CREATE INDEX IF NOT EXISTS "idx_api_summary_400f73" ON "api" ("summary");
CREATE INDEX IF NOT EXISTS "idx_api_tags_04ae27" ON "api" ("tags");
COMMENT ON COLUMN "api"."path" IS 'API路径';
COMMENT ON COLUMN "api"."method" IS '请求方法';
COMMENT ON COLUMN "api"."summary" IS '请求简介';
COMMENT ON COLUMN "api"."tags" IS 'API标签';
CREATE TABLE IF NOT EXISTS "audit_log" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL,
    "username" VARCHAR(64) NOT NULL DEFAULT '',
    "module" VARCHAR(64) NOT NULL DEFAULT '',
    "summary" VARCHAR(128) NOT NULL DEFAULT '',
    "method" VARCHAR(10) NOT NULL DEFAULT '',
    "path" VARCHAR(255) NOT NULL DEFAULT '',
    "status" INT NOT NULL DEFAULT -1,
    "response_time" INT NOT NULL DEFAULT 0,
    "request_args" JSONB,
    "response_body" JSONB
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
COMMENT ON COLUMN "audit_log"."user_id" IS '用户ID';
COMMENT ON COLUMN "audit_log"."username" IS '用户名称';
COMMENT ON COLUMN "audit_log"."module" IS '功能模块';
COMMENT ON COLUMN "audit_log"."summary" IS '请求描述';
COMMENT ON COLUMN "audit_log"."method" IS '请求方法';
COMMENT ON COLUMN "audit_log"."path" IS '请求路径';
COMMENT ON COLUMN "audit_log"."status" IS '状态码';
COMMENT ON COLUMN "audit_log"."response_time" IS '响应时间(单位ms)';
COMMENT ON COLUMN "audit_log"."request_args" IS '请求参数';
COMMENT ON COLUMN "audit_log"."response_body" IS '返回数据';
CREATE TABLE IF NOT EXISTS "dept" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "desc" VARCHAR(500),
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "order" INT NOT NULL DEFAULT 0,
    "parent_id" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_dept_created_4b11cf" ON "dept" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_dept_updated_0c0bd1" ON "dept" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_dept_name_c2b9da" ON "dept" ("name");
CREATE INDEX IF NOT EXISTS "idx_dept_is_dele_466228" ON "dept" ("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_dept_order_ddabe1" ON "dept" ("order");
CREATE INDEX IF NOT EXISTS "idx_dept_parent__a71a57" ON "dept" ("parent_id");
COMMENT ON COLUMN "dept"."name" IS '部门名称';
COMMENT ON COLUMN "dept"."desc" IS '备注';
COMMENT ON COLUMN "dept"."is_deleted" IS '软删除标记';
COMMENT ON COLUMN "dept"."order" IS '排序';
COMMENT ON COLUMN "dept"."parent_id" IS '父部门ID';
CREATE TABLE IF NOT EXISTS "deptclosure" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ancestor" INT NOT NULL,
    "descendant" INT NOT NULL,
    "level" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_deptclosure_created_96f6ef" ON "deptclosure" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_updated_41fc08" ON "deptclosure" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_ancesto_fbc4ce" ON "deptclosure" ("ancestor");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_descend_2ae8b1" ON "deptclosure" ("descendant");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_level_ae16b2" ON "deptclosure" ("level");
COMMENT ON COLUMN "deptclosure"."ancestor" IS '父代';
COMMENT ON COLUMN "deptclosure"."descendant" IS '子代';
COMMENT ON COLUMN "deptclosure"."level" IS '深度';
CREATE TABLE IF NOT EXISTS "file_mapping" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file_id" VARCHAR(255) NOT NULL UNIQUE,
    "original_filename" VARCHAR(255) NOT NULL,
    "file_type" VARCHAR(50) NOT NULL,
    "file_size" BIGINT,
    "upload_user_id" INT NOT NULL,
    "file_path" VARCHAR(500)
);
CREATE INDEX IF NOT EXISTS "idx_file_mappin_created_519929" ON "file_mapping" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_updated_621dab" ON "file_mapping" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_file_id_35e02a" ON "file_mapping" ("file_id");
CREATE INDEX IF NOT EXISTS "idx_file_mappin_upload__3562e4" ON "file_mapping" ("upload_user_id");
COMMENT ON COLUMN "file_mapping"."file_id" IS '文件ID';
COMMENT ON COLUMN "file_mapping"."original_filename" IS '原始文件名';
COMMENT ON COLUMN "file_mapping"."file_type" IS '文件类型';
COMMENT ON COLUMN "file_mapping"."file_size" IS '文件大小(字节)';
COMMENT ON COLUMN "file_mapping"."upload_user_id" IS '上传用户ID';
COMMENT ON COLUMN "file_mapping"."file_path" IS '本地文件路径';
COMMENT ON TABLE "file_mapping" IS '文件映射模型 - 管理文件ID和文件信息的映射关系';
CREATE TABLE IF NOT EXISTS "menu" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL,
    "remark" JSONB,
    "menu_type" VARCHAR(7),
    "icon" VARCHAR(100),
    "path" VARCHAR(100) NOT NULL,
    "order" INT NOT NULL DEFAULT 0,
    "parent_id" INT NOT NULL DEFAULT 0,
    "is_hidden" BOOL NOT NULL DEFAULT False,
    "component" VARCHAR(100) NOT NULL,
    "keepalive" BOOL NOT NULL DEFAULT True,
    "redirect" VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS "idx_menu_created_b6922b" ON "menu" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_menu_updated_e6b0a1" ON "menu" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_menu_name_b9b853" ON "menu" ("name");
CREATE INDEX IF NOT EXISTS "idx_menu_path_bf95b2" ON "menu" ("path");
CREATE INDEX IF NOT EXISTS "idx_menu_order_606068" ON "menu" ("order");
CREATE INDEX IF NOT EXISTS "idx_menu_parent__bebd15" ON "menu" ("parent_id");
COMMENT ON COLUMN "menu"."name" IS '菜单名称';
COMMENT ON COLUMN "menu"."remark" IS '保留字段';
COMMENT ON COLUMN "menu"."menu_type" IS '菜单类型';
COMMENT ON COLUMN "menu"."icon" IS '菜单图标';
COMMENT ON COLUMN "menu"."path" IS '菜单路径';
COMMENT ON COLUMN "menu"."order" IS '排序';
COMMENT ON COLUMN "menu"."parent_id" IS '父菜单ID';
COMMENT ON COLUMN "menu"."is_hidden" IS '是否隐藏';
COMMENT ON COLUMN "menu"."component" IS '组件';
COMMENT ON COLUMN "menu"."keepalive" IS '存活';
COMMENT ON COLUMN "menu"."redirect" IS '重定向';
CREATE TABLE IF NOT EXISTS "role" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "desc" VARCHAR(500)
);
CREATE INDEX IF NOT EXISTS "idx_role_created_7f5f71" ON "role" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_role_updated_5dd337" ON "role" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_role_name_e5618b" ON "role" ("name");
COMMENT ON COLUMN "role"."name" IS '角色名称';
COMMENT ON COLUMN "role"."desc" IS '角色描述';
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "alias" VARCHAR(30),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone" VARCHAR(20),
    "password" VARCHAR(128),
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_superuser" BOOL NOT NULL DEFAULT False,
    "last_login" TIMESTAMPTZ,
    "dept_id" INT
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
COMMENT ON COLUMN "user"."username" IS '用户名称';
COMMENT ON COLUMN "user"."alias" IS '姓名';
COMMENT ON COLUMN "user"."email" IS '邮箱';
COMMENT ON COLUMN "user"."phone" IS '电话';
COMMENT ON COLUMN "user"."password" IS '密码';
COMMENT ON COLUMN "user"."is_active" IS '是否激活';
COMMENT ON COLUMN "user"."is_superuser" IS '是否为超级管理员';
COMMENT ON COLUMN "user"."last_login" IS '最后登录时间';
COMMENT ON COLUMN "user"."dept_id" IS '部门ID';
CREATE TABLE IF NOT EXISTS "project" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "industry" VARCHAR(50),
    "status" VARCHAR(8) NOT NULL DEFAULT 'active',
    "total_images" INT NOT NULL DEFAULT 0,
    "annotated_images" INT NOT NULL DEFAULT 0,
    "total_annotations" INT NOT NULL DEFAULT 0,
    "created_by_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_project_created_efca31" ON "project" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_project_updated_d3b2ab" ON "project" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_project_name_4d952a" ON "project" ("name");
CREATE INDEX IF NOT EXISTS "idx_project_industr_d52dde" ON "project" ("industry");
CREATE INDEX IF NOT EXISTS "idx_project_status_d181f7" ON "project" ("status");
CREATE INDEX IF NOT EXISTS "idx_project_name_817ef1" ON "project" ("name", "status");
CREATE INDEX IF NOT EXISTS "idx_project_industr_4e5775" ON "project" ("industry", "status");
CREATE INDEX IF NOT EXISTS "idx_project_created_441fbb" ON "project" ("created_by_id", "status");
COMMENT ON COLUMN "project"."name" IS '项目名称';
COMMENT ON COLUMN "project"."description" IS '项目描述';
COMMENT ON COLUMN "project"."industry" IS '所属行业';
COMMENT ON COLUMN "project"."status" IS '项目状态';
COMMENT ON COLUMN "project"."total_images" IS '总图片数';
COMMENT ON COLUMN "project"."annotated_images" IS '已标注图片数';
COMMENT ON COLUMN "project"."total_annotations" IS '总标注数';
COMMENT ON COLUMN "project"."created_by_id" IS '创建者';
COMMENT ON TABLE "project" IS '项目模型 - 管理AI开发项目';
CREATE TABLE IF NOT EXISTS "dataset" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "version" VARCHAR(20) NOT NULL,
    "dataset_type" VARCHAR(21) NOT NULL DEFAULT 'instance_segmentation',
    "split_config" JSONB NOT NULL,
    "total_images" INT NOT NULL DEFAULT 0,
    "train_images" INT NOT NULL DEFAULT 0,
    "val_images" INT NOT NULL DEFAULT 0,
    "test_images" INT NOT NULL DEFAULT 0,
    "created_by_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "project_id" BIGINT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_dataset_project_485b7f" UNIQUE ("project_id", "name", "version")
);
CREATE INDEX IF NOT EXISTS "idx_dataset_created_aa3c3b" ON "dataset" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_dataset_updated_6d60df" ON "dataset" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_dataset_name_17311f" ON "dataset" ("name");
CREATE INDEX IF NOT EXISTS "idx_dataset_version_ccebd2" ON "dataset" ("version");
CREATE INDEX IF NOT EXISTS "idx_dataset_project_114497" ON "dataset" ("project_id", "dataset_type");
CREATE INDEX IF NOT EXISTS "idx_dataset_version_519d2c" ON "dataset" ("version", "dataset_type");
COMMENT ON COLUMN "dataset"."name" IS '数据集名称';
COMMENT ON COLUMN "dataset"."description" IS '数据集描述';
COMMENT ON COLUMN "dataset"."version" IS '版本号';
COMMENT ON COLUMN "dataset"."dataset_type" IS '数据集类型';
COMMENT ON COLUMN "dataset"."split_config" IS '数据集分割配置';
COMMENT ON COLUMN "dataset"."total_images" IS '总图片数';
COMMENT ON COLUMN "dataset"."train_images" IS '训练图片数';
COMMENT ON COLUMN "dataset"."val_images" IS '验证图片数';
COMMENT ON COLUMN "dataset"."test_images" IS '测试图片数';
COMMENT ON COLUMN "dataset"."created_by_id" IS '创建者';
COMMENT ON COLUMN "dataset"."project_id" IS '所属项目';
COMMENT ON TABLE "dataset" IS '数据集模型 - 管理训练数据集';
CREATE TABLE IF NOT EXISTS "image_library" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "image_count" INT NOT NULL DEFAULT 0,
    "total_size" BIGINT NOT NULL DEFAULT 0,
    "supported_formats" JSONB NOT NULL,
    "max_image_size" BIGINT NOT NULL DEFAULT 10485760,
    "project_id" BIGINT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_image_libra_project_55f000" UNIQUE ("project_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_image_libra_created_5b618b" ON "image_library" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_image_libra_updated_e9ebfa" ON "image_library" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_image_libra_name_ee5b16" ON "image_library" ("name");
CREATE INDEX IF NOT EXISTS "idx_image_libra_project_55f000" ON "image_library" ("project_id", "name");
COMMENT ON COLUMN "image_library"."name" IS '图库名称';
COMMENT ON COLUMN "image_library"."description" IS '图库描述';
COMMENT ON COLUMN "image_library"."image_count" IS '图片数量';
COMMENT ON COLUMN "image_library"."total_size" IS '总大小(字节)';
COMMENT ON COLUMN "image_library"."supported_formats" IS '支持的图片格式';
COMMENT ON COLUMN "image_library"."max_image_size" IS '最大图片大小(字节)';
COMMENT ON COLUMN "image_library"."project_id" IS '所属项目';
COMMENT ON TABLE "image_library" IS '图库模型 - 管理项目中的图片资源';
CREATE TABLE IF NOT EXISTS "image_item" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "width" INT NOT NULL,
    "height" INT NOT NULL,
    "format" VARCHAR(10) NOT NULL,
    "annotation_status" VARCHAR(11) NOT NULL DEFAULT 'pending',
    "annotated_by_id" BIGINT REFERENCES "user" ("id") ON DELETE CASCADE,
    "file_mapping_id" BIGINT NOT NULL REFERENCES "file_mapping" ("id") ON DELETE CASCADE,
    "image_library_id" BIGINT NOT NULL REFERENCES "image_library" ("id") ON DELETE CASCADE,
    "reviewed_by_id" BIGINT REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_image_item_created_4d1cf9" ON "image_item" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_image_item_updated_d942c5" ON "image_item" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_image_item_format_e65c1c" ON "image_item" ("format");
CREATE INDEX IF NOT EXISTS "idx_image_item_annotat_ffa54a" ON "image_item" ("annotation_status");
CREATE INDEX IF NOT EXISTS "idx_image_item_image_l_8dd965" ON "image_item" ("image_library_id", "annotation_status");
CREATE INDEX IF NOT EXISTS "idx_image_item_annotat_7a41fe" ON "image_item" ("annotated_by_id", "annotation_status");
CREATE INDEX IF NOT EXISTS "idx_image_item_format_31a4e4" ON "image_item" ("format", "annotation_status");
COMMENT ON COLUMN "image_item"."width" IS '宽度';
COMMENT ON COLUMN "image_item"."height" IS '高度';
COMMENT ON COLUMN "image_item"."format" IS '图片格式';
COMMENT ON COLUMN "image_item"."annotation_status" IS '标注状态';
COMMENT ON COLUMN "image_item"."annotated_by_id" IS '标注者';
COMMENT ON COLUMN "image_item"."file_mapping_id" IS '文件映射';
COMMENT ON COLUMN "image_item"."image_library_id" IS '所属图库';
COMMENT ON COLUMN "image_item"."reviewed_by_id" IS '审核者';
COMMENT ON TABLE "image_item" IS '图片条目模型 - 管理单个图片文件';
CREATE TABLE IF NOT EXISTS "label_group" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "color" VARCHAR(7) NOT NULL DEFAULT '#FF0000',
    "project_id" BIGINT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_label_group_project_906ebb" UNIQUE ("project_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_label_group_created_019522" ON "label_group" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_label_group_updated_9b7822" ON "label_group" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_label_group_name_e8401d" ON "label_group" ("name");
CREATE INDEX IF NOT EXISTS "idx_label_group_project_906ebb" ON "label_group" ("project_id", "name");
COMMENT ON COLUMN "label_group"."name" IS '标签组名称';
COMMENT ON COLUMN "label_group"."description" IS '描述';
COMMENT ON COLUMN "label_group"."color" IS '颜色';
COMMENT ON COLUMN "label_group"."project_id" IS '所属项目';
COMMENT ON TABLE "label_group" IS '标签组模型 - 管理标注类别';
CREATE TABLE IF NOT EXISTS "annotation" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "annotation_data" JSONB NOT NULL,
    "annotation_type" VARCHAR(21) NOT NULL DEFAULT 'instance_segmentation',
    "confidence" DOUBLE PRECISION NOT NULL DEFAULT 1,
    "created_by_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "image_item_id" BIGINT NOT NULL REFERENCES "image_item" ("id") ON DELETE CASCADE,
    "label_group_id" BIGINT NOT NULL REFERENCES "label_group" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_annotation_created_e0d5ec" ON "annotation" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_annotation_updated_997b25" ON "annotation" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_annotation_image_i_18d423" ON "annotation" ("image_item_id", "label_group_id");
CREATE INDEX IF NOT EXISTS "idx_annotation_created_548589" ON "annotation" ("created_by_id", "annotation_type");
COMMENT ON COLUMN "annotation"."annotation_data" IS '标注数据';
COMMENT ON COLUMN "annotation"."annotation_type" IS '标注类型';
COMMENT ON COLUMN "annotation"."confidence" IS '置信度';
COMMENT ON COLUMN "annotation"."created_by_id" IS '创建者';
COMMENT ON COLUMN "annotation"."image_item_id" IS '图片条目';
COMMENT ON COLUMN "annotation"."label_group_id" IS '标签组';
COMMENT ON TABLE "annotation" IS '标注模型 - 管理图片标注信息';
CREATE TABLE IF NOT EXISTS "project_member" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "role" VARCHAR(6) NOT NULL DEFAULT 'member',
    "joined_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" BIGINT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_project_mem_project_5d4951" UNIQUE ("project_id", "user_id")
);
CREATE INDEX IF NOT EXISTS "idx_project_mem_created_b2a25b" ON "project_member" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_project_mem_updated_8e5894" ON "project_member" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_project_mem_project_5633ff" ON "project_member" ("project_id", "role");
CREATE INDEX IF NOT EXISTS "idx_project_mem_user_id_cf260e" ON "project_member" ("user_id", "role");
COMMENT ON COLUMN "project_member"."role" IS '角色';
COMMENT ON COLUMN "project_member"."joined_at" IS '加入时间';
COMMENT ON COLUMN "project_member"."project_id" IS '项目';
COMMENT ON COLUMN "project_member"."user_id" IS '用户';
COMMENT ON TABLE "project_member" IS '项目成员模型 - 管理项目成员和权限';
CREATE TABLE IF NOT EXISTS "solution" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "model_config" JSONB NOT NULL,
    "training_config" JSONB NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_by_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "project_id" BIGINT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_solution_project_97f426" UNIQUE ("project_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_solution_created_854ad7" ON "solution" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_solution_updated_372dc0" ON "solution" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_solution_name_822718" ON "solution" ("name");
CREATE INDEX IF NOT EXISTS "idx_solution_project_a70a69" ON "solution" ("project_id", "is_active");
COMMENT ON COLUMN "solution"."name" IS '方案名称';
COMMENT ON COLUMN "solution"."description" IS '方案描述';
COMMENT ON COLUMN "solution"."model_config" IS '模型配置';
COMMENT ON COLUMN "solution"."training_config" IS '训练配置';
COMMENT ON COLUMN "solution"."is_active" IS '是否激活';
COMMENT ON COLUMN "solution"."created_by_id" IS '创建者';
COMMENT ON COLUMN "solution"."project_id" IS '所属项目';
COMMENT ON TABLE "solution" IS '方案模型 - 管理AI训练方案';
CREATE TABLE IF NOT EXISTS "training_task" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "task_name" VARCHAR(100) NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'pending',
    "training_config" JSONB NOT NULL,
    "docker_image" VARCHAR(200) NOT NULL,
    "progress" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "current_epoch" INT NOT NULL DEFAULT 0,
    "total_epochs" INT NOT NULL DEFAULT 100,
    "log_file_path" VARCHAR(500),
    "error_message" TEXT,
    "started_at" TIMESTAMPTZ,
    "completed_at" TIMESTAMPTZ,
    "created_by_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "dataset_id" BIGINT NOT NULL REFERENCES "dataset" ("id") ON DELETE CASCADE,
    "solution_id" BIGINT NOT NULL REFERENCES "solution" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_training_ta_created_edf20c" ON "training_task" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_training_ta_updated_d356f9" ON "training_task" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_training_ta_task_na_1e2f4c" ON "training_task" ("task_name");
CREATE INDEX IF NOT EXISTS "idx_training_ta_status_bae8f7" ON "training_task" ("status");
CREATE INDEX IF NOT EXISTS "idx_training_ta_solutio_7a488e" ON "training_task" ("solution_id", "status");
CREATE INDEX IF NOT EXISTS "idx_training_ta_dataset_c12bc5" ON "training_task" ("dataset_id", "status");
CREATE INDEX IF NOT EXISTS "idx_training_ta_created_8e7c44" ON "training_task" ("created_by_id", "status");
COMMENT ON COLUMN "training_task"."task_name" IS '任务名称';
COMMENT ON COLUMN "training_task"."status" IS '训练状态';
COMMENT ON COLUMN "training_task"."training_config" IS '训练配置';
COMMENT ON COLUMN "training_task"."docker_image" IS 'Docker镜像';
COMMENT ON COLUMN "training_task"."progress" IS '训练进度';
COMMENT ON COLUMN "training_task"."current_epoch" IS '当前epoch';
COMMENT ON COLUMN "training_task"."total_epochs" IS '总epoch数';
COMMENT ON COLUMN "training_task"."log_file_path" IS '日志文件路径';
COMMENT ON COLUMN "training_task"."error_message" IS '错误信息';
COMMENT ON COLUMN "training_task"."started_at" IS '开始时间';
COMMENT ON COLUMN "training_task"."completed_at" IS '完成时间';
COMMENT ON COLUMN "training_task"."created_by_id" IS '创建者';
COMMENT ON COLUMN "training_task"."dataset_id" IS '训练数据集';
COMMENT ON COLUMN "training_task"."solution_id" IS '训练方案';
COMMENT ON TABLE "training_task" IS '训练任务模型 - 管理模型训练任务';
CREATE TABLE IF NOT EXISTS "model_version" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "version" VARCHAR(50) NOT NULL,
    "model_name" VARCHAR(100) NOT NULL,
    "model_path" VARCHAR(500) NOT NULL,
    "status" VARCHAR(8) NOT NULL DEFAULT 'training',
    "metrics" JSONB,
    "model_size" BIGINT,
    "deployment_config" JSONB,
    "training_task_id" BIGINT NOT NULL REFERENCES "training_task" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_model_versi_trainin_d0721d" UNIQUE ("training_task_id", "version")
);
CREATE INDEX IF NOT EXISTS "idx_model_versi_created_4487fc" ON "model_version" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_model_versi_updated_e1f1d8" ON "model_version" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_model_versi_version_4e8951" ON "model_version" ("version");
CREATE INDEX IF NOT EXISTS "idx_model_versi_status_aaa196" ON "model_version" ("status");
CREATE INDEX IF NOT EXISTS "idx_model_versi_trainin_6f1630" ON "model_version" ("training_task_id", "status");
CREATE INDEX IF NOT EXISTS "idx_model_versi_version_8f8121" ON "model_version" ("version", "status");
COMMENT ON COLUMN "model_version"."version" IS '模型版本';
COMMENT ON COLUMN "model_version"."model_name" IS '模型名称';
COMMENT ON COLUMN "model_version"."model_path" IS '模型文件路径';
COMMENT ON COLUMN "model_version"."status" IS '模型状态';
COMMENT ON COLUMN "model_version"."metrics" IS '评估指标';
COMMENT ON COLUMN "model_version"."model_size" IS '模型大小(字节)';
COMMENT ON COLUMN "model_version"."deployment_config" IS '部署配置';
COMMENT ON COLUMN "model_version"."training_task_id" IS '训练任务';
COMMENT ON TABLE "model_version" IS '模型版本模型 - 管理训练产生的模型版本';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "role_api" (
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "api_id" BIGINT NOT NULL REFERENCES "api" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_role_api_role_id_ba4286" ON "role_api" ("role_id", "api_id");
CREATE TABLE IF NOT EXISTS "role_menu" (
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "menu_id" BIGINT NOT NULL REFERENCES "menu" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_role_menu_role_id_90801c" ON "role_menu" ("role_id", "menu_id");
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" BIGINT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_user_role_user_id_d0bad3" ON "user_role" ("user_id", "role_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
