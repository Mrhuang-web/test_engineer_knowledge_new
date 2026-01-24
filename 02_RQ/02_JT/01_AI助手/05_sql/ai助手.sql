SELECT * FROM resource_schema WHERE resource = 'ai_assistant';
SELECT * FROM resource_schema_actions WHERE  resource = 'ai_assistant';


INSERT INTO `resource_schema`(`resource`, `general`, `created_at`, `name`, `parent_resource`) VALUES ('ai_assistant', 'f', '2025-07-17 08:10:52.000000', 'AI助手', 'all');

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:answers', '智能问答', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:view', '查看', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:update', '修改', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:delete', '删除', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:uploadFile', '文件上传', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:deleteFile', '文件删除', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:deleteParagraph', '段落删除', 1);

INSERT INTO `resource_schema_actions`(`resource`, `action`, `action_name`, `action_type`) VALUES ('ai_assistant', 'ai_assistant:addParagraph', '新增段落', 1);



