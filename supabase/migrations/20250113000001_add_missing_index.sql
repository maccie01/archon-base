-- Add missing index for parent_task_id foreign key
-- This improves performance when querying subtasks

CREATE INDEX IF NOT EXISTS idx_archon_tasks_parent_task_id
ON public.archon_tasks(parent_task_id);

-- Comment explaining the index
COMMENT ON INDEX idx_archon_tasks_parent_task_id IS
'Index on parent_task_id foreign key for efficient subtask queries';
