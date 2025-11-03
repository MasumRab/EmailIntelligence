---
id: task-architecture-implement-rw-notmuch-datasource
title: Implement Read-Write NotmuchDataSource
status: To Do
assignee: []
created_date: '2025-11-02'
labels: [backend, architecture, datasource]
dependencies: []
parent_task_id: 'task-architecture-improvement'
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The current `NotmuchDataSource` is read-only, which means that several of the methods in the `DataSource` interface (e.g., `create_email`, `delete_email`, `update_email`) are not implemented. This creates an inconsistent implementation and limits the functionality of the application when using `notmuch` as a data source.

This task is to implement a "read-write" `NotmuchDataSource` that can handle both read and write operations.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement `create_email` in `NotmuchDataSource` by adding a new email file and indexing it with notmuch.
- [ ] #2 Implement `update_email` and `update_email_by_message_id` by using notmuch tags to reflect changes (e.g., adding `unread` tag).
- [ ] #3 Implement `delete_email` by adding a `deleted` tag to the email in notmuch. The email file itself should probably not be deleted from the filesystem, just tagged.
- [ ] #4 Implement `create_category` by mapping it to notmuch tags.
- [ ] #5 All methods defined in the `DataSource` abstract base class are fully implemented in `NotmuchDataSource`.
- [ ] #6 The implementation is covered by unit tests.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
The implementation should leverage the `notmuch` library's tagging feature to simulate write operations. For example:
- **Deleting an email:** Add a `deleted` tag.
- **Marking as read/unread:** Add or remove the `unread` tag.
- **Categorizing:** Add a tag corresponding to the category name.
- **Creating an email:** This is more complex. It would involve writing the email content to a file in a location that notmuch can index, and then triggering a `notmuch new` command to index it. The application will need appropriate permissions and configuration to do this.

This approach will provide a more complete and consistent implementation of the `DataSource` interface and will unlock the full functionality of the application when using `notmuch` as a data source.
<!-- SECTION:NOTES:END -->
