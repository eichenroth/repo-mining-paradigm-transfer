-- earliest project
-- runtime: < 24h

CREATE MATERIALIZED VIEW earliest_project AS WITH existing_projects AS (
         SELECT p.id,
            p.created_at
           FROM projects p
          WHERE (p.deleted = 0)
        ), existing_project_commits AS (
         SELECT pc.commit_id,
            pc.project_id,
            ep.created_at
           FROM (project_commits pc
             JOIN existing_projects ep ON ((pc.project_id = ep.id)))
        ), min_created_at_commit AS (
         SELECT existing_project_commits.commit_id,
            min(existing_project_commits.created_at) AS created_at
           FROM existing_project_commits
          GROUP BY existing_project_commits.commit_id
        ), min_created_at_project_commits AS (
         SELECT epc.commit_id,
            epc.project_id
           FROM (existing_project_commits epc
             JOIN min_created_at_commit mcac ON (((epc.commit_id = mcac.commit_id) AND (epc.created_at = mcac.created_at))))
        )
 SELECT commits.sha,
    mcapc.commit_id,
    min(mcapc.project_id) AS project_id
   FROM (min_created_at_project_commits mcapc
     JOIN commits ON ((mcapc.commit_id = commits.id)))
  GROUP BY commits.sha, mcapc.commit_id;

create unique index earliest_project_sha
  ON earliest_project (sha);

CREATE UNIQUE INDEX earliest_project_commit_id
  ON earliest_project (commit_id);

CREATE INDEX earliest_project_project_id
  ON earliest_project (project_id);


-- loc commit file extension
-- runtime: ~ 7 days

CREATE MATERIALIZED VIEW loc_commit_file_ext AS WITH commit_file_extensions AS (
    SELECT
      raw_patches.sha,
      regexp_replace(raw_patches.name, '^.*\.' :: text, '' :: text) AS file_ext,
      (raw_patches.changes - raw_patches.deletions)                 AS additions,
      raw_patches.deletions
    FROM raw_patches
    WHERE (raw_patches.name ~ '\.' :: text)
)
SELECT
  commit_file_extensions.sha,
  commit_file_extensions.file_ext,
  sum(commit_file_extensions.additions) AS additions,
  sum(commit_file_extensions.deletions) AS deletions
FROM commit_file_extensions
GROUP BY commit_file_extensions.sha, commit_file_extensions.file_ext;

CREATE INDEX loc_commit_file_ext_sha
  ON loc_commit_file_ext (sha);


-- loc user file extension
-- runtime: < 12h

CREATE MATERIALIZED VIEW loc_user_file_ext AS SELECT u.id AS user_id,
    u.login,
    loc.file_ext,
    sum(loc.additions) AS additions,
    sum(loc.deletions) AS deletions
   FROM ((users u
     JOIN commits c ON ((u.id = c.author_id)))
     JOIN loc_commit_file_ext loc ON ((c.sha = (loc.sha)::text)))
  GROUP BY u.id, u.login, loc.file_ext;


-- candidates java
-- runtime < 12h

CREATE MATERIALIZED VIEW candidates_java_py AS WITH loc_commit_java_py AS (
         SELECT lcfe.sha,
            lcfe.file_ext,
            lcfe.additions,
            lcfe.deletions
           FROM loc_commit_file_ext lcfe
          WHERE ((lcfe.file_ext = 'java'::text) OR (lcfe.file_ext = 'py'::text))
        )
 SELECT c.sha,
    c.author_id,
    c.created_at,
    lcjp.file_ext,
    lcjp.additions,
    lcjp.deletions,
    p.name AS project_name,
    u.login AS owner
   FROM ((((commits c
     JOIN loc_commit_java_py lcjp ON ((c.sha = (lcjp.sha)::text)))
     JOIN earliest_project ep ON (((lcjp.sha)::text = ep.sha)))
     JOIN projects p ON ((ep.project_id = p.id)))
     JOIN users u ON ((p.owner_id = u.id)));


-- candidates cpp
-- runtime < 12h

CREATE MATERIALIZED VIEW candidates_cpp_py AS WITH loc_commit_cpp_py AS (
         SELECT lcfe.sha,
            lcfe.file_ext,
            lcfe.additions,
            lcfe.deletions
           FROM loc_commit_file_ext lcfe
          WHERE ((lcfe.file_ext = 'cpp'::text) OR (lcfe.file_ext = 'py'::text))
        )
 SELECT c.sha,
    c.author_id,
    c.created_at,
    lcjp.file_ext,
    lcjp.additions,
    lcjp.deletions,
    p.name AS project_name,
    u.login AS owner
   FROM ((((commits c
     JOIN loc_commit_cpp_py lcjp ON ((c.sha = (lcjp.sha)::text)))
     JOIN earliest_project ep ON (((lcjp.sha)::text = ep.sha)))
     JOIN projects p ON ((ep.project_id = p.id)))
     JOIN users u ON ((p.owner_id = u.id)));

create index candidates_cpp_py_author_id
  on candidates_cpp_py (author_id);


-- candidates functional languages
-- runtime < 12h

CREATE MATERIALIZED VIEW candidates_fun_py AS WITH loc_commit_fun_py AS (
         SELECT lcfe.sha,
            lcfe.file_ext,
            lcfe.additions,
            lcfe.deletions
           FROM loc_commit_file_ext lcfe
          WHERE (((((((((((lcfe.file_ext = 'hs'::text) OR (lcfe.file_ext = 'lhs'::text)) OR (lcfe.file_ext = 'erl'::text)) OR (lcfe.file_ext = 'hrl'::text)) OR (lcfe.file_ext = 'lisp'::text)) OR (lcfe.file_ext = 'lsp'::text)) OR (lcfe.file_ext = 'clj'::text)) OR (lcfe.file_ext = 'cljs'::text)) OR (lcfe.file_ext = 'cljc'::text)) OR (lcfe.file_ext = 'edu'::text)) OR (lcfe.file_ext = 'py'::text))
        )
 SELECT c.sha,
    c.author_id,
    c.created_at,
    lcfp.file_ext,
    lcfp.additions,
    lcfp.deletions,
    p.name AS project_name,
    u.login AS owner
   FROM ((((commits c
     JOIN loc_commit_fun_py lcfp ON ((c.sha = (lcfp.sha)::text)))
     JOIN earliest_project ep ON (((lcfp.sha)::text = ep.sha)))
     JOIN projects p ON ((ep.project_id = p.id)))
     JOIN users u ON ((p.owner_id = u.id)));

create index candidates_fun_py_author_id
  on candidates_fun_py (author_id);
