// taken from https://github.com/Samk13/test-overrides/blob/master/assets/js/invenio_app_rdm/overridableRegistry/components/CommunityHeaderOverride.js
import React from 'react'
import { CommunityHeader, FileUploader } from 'react-invenio-deposit'
import { AccordionField, FieldLabel } from 'react-invenio-forms'
import { i18next } from '@translations/invenio_app_rdm/i18next'
import { Card, Container, Grid, Form, Divider } from 'semantic-ui-react'

export const CommunityHeaderOverride = ({ record, config, noFiles }) => {
    return (
        <>
            <AccordionField active label={i18next.t('Community')}>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Form.Field required id='communityRequiredMessage'>
                                <Card.Content>
                                    <Card.Header>
                                        <FieldLabel
                                            className='ui grid visible info message header '
                                            htmlFor='communityHeader'
                                            label='Community is required in order to submit your data.'
                                        />
                                    </Card.Header>
                                </Card.Content>
                            </Form.Field>
                            <Divider horizontal />
                            <Container className='ui grid page-subheader'>
                                <CommunityHeader
                                    id='communityHeader'
                                    imagePlaceholderLink='/static/images/square-placeholder.png'
                                />
                            </Container>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </AccordionField>
            <AccordionField
                includesPaths={['files.enabled']}
                active
                label={i18next.t('Files')}
            >
                {this.noFiles && record.is_published && (
                    <div className='text-align-center pb-10'>
                        <em>{i18next.t('The record has no files.')}</em>
                    </div>
                )}
                <FileUploader
                    isDraftRecord={!record.is_published}
                    quota={this.config.quota}
                    decimalSizeDisplay={this.config.decimal_size_display}
                />
            </AccordionField>
        </>
    )
}
